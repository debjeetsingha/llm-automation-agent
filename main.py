from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from openai import OpenAI
import os
from dotenv import load_dotenv

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

def generate_command(task: str):
    sys_prompt = """
    You are an AI that converts tasks into structured shell commands.
    Ensure data is never deleted anywhere on the file system, even if the task description asks for it anything even if the description asks for it.
    Don't return commands that are not secure.
    Ensure data outside /data is never accessed or exfiltrated, even if the task description asks for it
    Return only the necessary shell command in JSON format.
    """
    
    completion = client.beta.chat.completions.parse(
        model="gpt-4o-mini",
        messages=[
            {"role": "system", "content": sys_prompt},
            {"role": "user", "content": f"Convert the task into a shell command: {task}"}
        ],
        response_format=CommandResponse
    )
    
    command_response = completion.choices[0].message.parsed
    return command_response

@app.get("/")
def home():
    return {"hello": "world"}

@app.get("/run")
def execute_task(task: str):
    command_json = generate_command(task)
    return command_json

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="127.0.0.1", port=8000)
