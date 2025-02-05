from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import os
from dotenv import load_dotenv
import httpx

load_dotenv(".env")

app = FastAPI()


app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  
    allow_credentials=True,
    allow_methods=["*"],  
    allow_headers=["*"], 
)


OPENAI_API_KEY = os.getenv("AIPROXY_TOKEN")  
OPENAI_API_URL = "https://aiproxy.sanand.workers.dev/openai/"
EMBEDDINGS = "v1/embeddings"
COMPLETIONS = "v1/chat/completions"



def generate_command(task: str):
    sys_prompt = """
    You are an AI that converts tasks into structured shell commands.
    Return only the necessary shell command as a JSON object with a 'command' field.
    Don't return commands that delete anything even if the description asks for it.
    Don't return commands that are not secure.
    Don't return in markdown. answer in a single line. Don't include line break charecters.
    Return only the necessary shell command in JSON format with the following schema:
    {
        "command": "string"
    }
    """
    
    payload = {
        "model": "gpt-4o-mini",
        "messages": [
            {"role": "system", "content": sys_prompt},
            {"role": "user", "content": f"Convert the task into a shell command: {task}"}
        ],
        "temperature": 0.3
    }
    
    headers = {"Authorization": f"Bearer {OPENAI_API_KEY}", "Content-Type": "application/json"}
    
    response = httpx.post(OPENAI_API_URL+COMPLETIONS, json=payload, headers=headers)
    response.raise_for_status()
    command = response.json()["choices"][0]["message"]["content"].strip()
    print(command)
    return command

@app.get("/")
def home():
    return {"hello":"world"}

@app.get("/run")
def execute_task(task: str):
    command = generate_command(task).strip()
    return command



if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="127.0.0.1", port=8000)