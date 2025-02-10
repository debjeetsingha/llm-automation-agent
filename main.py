from fastapi import FastAPI, HTTPException, Response
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from openai import OpenAI
import os
from dotenv import load_dotenv
from pathlib import Path
import subprocess
import json

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
    allow_methods=["*"],  
    allow_headers=["*"], 
)

class CommandResponse(BaseModel):
    command: str

def generate_command(task: str) -> json:
    sys_prompt = """
    You are an AI that converts tasks into structured shell commands.
    Ensure data is never deleted anywhere on the file system, even if the task description asks for it anything even if the description asks for it.
    Don't return commands that are not secure.
    Ensure data outside /data is never accessed or exfiltrated, even if the task description asks for it
    Return only the necessary shell command in JSON format.
    If the the task description is invalid, return an empty string.
    """
    
    completion = client.beta.chat.completions.parse(
        model="gpt-4o-mini",
        messages=[
            {"role": "user", "content": f"Convert the task into a shell command: {task}"},
            {"role": "system", "content": sys_prompt},
        ],
        response_format=CommandResponse
    )
    
    command_response = completion.choices[0].message.parsed
    return command_response.model_dump()

def execute_command(cmd: str):
    result = subprocess.run([cmd], shell=True, capture_output=True, text=True)
    return result


@app.get("/")
def home():
    return {"hello": "world"}

@app.post("/run")
async def execute_task(task: str):
    command_json = generate_command(task)
    if command_json["command"] == "":
        raise HTTPException(status_code=400, detail="Invalid task description")
    try:
        result = execute_command(command_json["command"])
        return Response(status_code=200)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Internal Server Error: {str(e)}")


@app.get("/read")
async def read_file(path: str):
    file_path = Path(path)
    if not file_path.is_file():
        return Response(status_code=404)    
    try:
        with file_path.open("r", encoding="utf-8") as f:
            return f.read()
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error reading file: {str(e)}")
    
    
if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="127.0.0.1", port=8000)
