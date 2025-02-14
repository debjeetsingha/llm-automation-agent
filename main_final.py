from fastapi import FastAPI, HTTPException, Response
from fastapi.middleware.cors import CORSMiddleware
import os
from dotenv import load_dotenv
from pathlib import Path
import json
from typing import Dict, Any, Optional
from openai import OpenAI

from process_task import execute_function, system_prompt
from function_definations import tools

load_dotenv(".env")

AIPROXY_TOKEN = os.getenv("AIPROXY_TOKEN")
API_BASE_URL = "https://aiproxy.sanand.workers.dev/openai/v1"

client = OpenAI(
    api_key=AIPROXY_TOKEN,
    base_url=API_BASE_URL
)

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  
    allow_credentials=True,
    allow_methods=["GET","POST"],  
    allow_headers=["*"], 
)

@app.get("/")
def home():
    return {"hello": "world"}

@app.get("/read")
async def read_file(path: str):
    # Ensure safe path resolution
    base_dir = Path("/data").resolve()  # Base directory
    file_path = (base_dir / path).resolve()  # Resolve to an absolute path

    # Check if the resolved path is still within the base directory
    if not file_path.is_file() or base_dir not in file_path.parents:
        return Response(status_code=404)
    
    try:
        with file_path.open("r", encoding="utf-8") as f:
            return Response(content=f.read(), media_type="text/plain")
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error reading file: {str(e)}")
    
@app.post("/run")
async def handle_task(task: str):
    messages = [
    {"role": "system", "content": system_prompt},
    {"role": "user", "content": task}
    ]

    while True:
        response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=messages,
        tools=tools,
        tool_choice="auto",
        parallel_tool_calls=False,
        )
        response_message = response.choices[0].message
        # if response_message.tool_calls:
        #     for tool_call in response_message.tool_calls:
        #         name = tool_call.function.name
        #         args = json.loads(tool_call.function.arguments)
                
        #         function_response = execute_function(name, args)
                
        #         messages.append({
        #             "role": "system",
        #             "content": str(function_response)
        #         })
        # else:
        #     return {"result": response_message.content}

        for tool_call in response_message.tool_calls:
            name = tool_call.function.name
            args = json.loads(tool_call.function.arguments)
            
            function_response = execute_function(name, args)
            return function_response
if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="127.0.0.1", port=8000)