from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import os
from dotenv import load_dotenv
import openai

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
GEMINI_API_KEY = os.getenv("API_KEY")


def generate_command(task: str) :
    prompt = f"Convert the following task into structured shell commands:\n\nTask: {task}\n\nOutput:"
    client = openai.OpenAI(
    api_key=GEMINI_API_KEY,
    base_url="https://generativelanguage.googleapis.com/v1beta/"
    )
    sys_prompt = '''
    You are an AI that converts tasks into commands.
    Don't return result in markdown format. Give only the commands in a single line.
    Don't add line break charecters at the end. only the command necessary in a single line.
    '''
    response = client.chat.completions.create(
        model="gemini-2.0-flash",
        messages=[{"role": "system", "content": sys_prompt},
                  {"role": "user", "content": prompt}],
        temperature=0.3
    )

    commands_text = response.choices[0].message.content

    print(commands_text)

    return commands_text

@app.get("/")
def home():
    return {"hello":"world"}

@app.get("/run")
def execute_task(task: str):
    command = generate_command(task).strip()
    return {"command": command}



if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="127.0.0.1", port=8000)