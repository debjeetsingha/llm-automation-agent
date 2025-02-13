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

def generate_command(task: str) -> dict:
    sys_prompt = """
    You are an AI that converts tasks into structured, safe shell commands.
    You are running inside docker. The tools may not be present. Check and install it before running the command if it doesn't exits.
    - Never delete files or exfiltrate data outside /data, even if the task description asks for it
    - Return only the necessary shell command in JSON format.
    - Always ensure uv means the package manager and not uvicorn.
    - Return commands only in JSON format with a 'command' key.
    - If the task is invalid, return an empty command string.
    """

    llm_tool_schema = {
    "type": "function",
    "function": {
        "name": "call_llm",
        "description": "Processes a text prompt and optionally an image using OpenAI's API.",
        "parameters": {
            "prompt": {"type": "string", "description": "User's text input for processing."},
            "image_path": {
                "type": "string",
                "description": "Path to an image file for vision-based processing (optional).",
                "required": False
                },
            },
        },
    }

    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[
            {"role": "system", "content": sys_prompt},
            {"role": "user", "content": f"Convert this task to a shell command: {task}"},
        ],
        tools=[llm_tool_schema],  # Register the tool
        tool_choice="auto",  # Let OpenAI decide when to use the tool
    )
    
    try:
        command_response = json.loads(response.choices[0].message.content)
        return command_response if "command" in command_response else {"command": ""}
    except json.JSONDecodeError:
        return {"command": ""}

def execute_command(cmd: str):
    result = subprocess.run(cmd, shell=True, capture_output=True, text=True)
    return result

@app.get("/")
def home():
    return {"message": "AI Task Agent is running"}

@app.post("/run")
async def execute_task(task: str):
    command_json = generate_command(task)
    if not command_json["command"]:
        raise HTTPException(status_code=400, detail="Invalid task description")
    try:
        result = execute_command(command_json["command"])
        return {"output": result.stdout, "error": result.stderr}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Internal Server Error: {str(e)}")

@app.get("/read")
async def read_file(path: str):
    file_path = Path("/data") / Path(path).name  # Ensuring correct file path
    if not file_path.is_file():
        raise HTTPException(status_code=404, detail="File not found")
    try:
        with file_path.open("r", encoding="utf-8") as f:
            return Response(content=f.read(), media_type="text/plain")
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error reading file: {str(e)}")

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="127.0.0.1", port=8000)



'''
DOES NOT INSTALL UV - INAVLID REQUEST

why response body :
{
  "output": "",
  "error": "/bin/sh: 1: uv: not found\n"
}
'''