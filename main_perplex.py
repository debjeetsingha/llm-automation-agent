from fastapi import FastAPI, HTTPException, Response
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import openai
import os
from dotenv import load_dotenv
from pathlib import Path
import subprocess
import json
import markdown
import sqlite3
from typing import List, Dict, Any

load_dotenv(".env")

AIPROXY_TOKEN = os.getenv("AIPROXY_TOKEN")
API_BASE_URL = "https://aiproxy.sanand.workers.dev/openai/v1"

client = openai.OpenAI(
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

# Function definitions

def markdown_to_html(markdown_text: str) -> str:
    return markdown.markdown(markdown_text)

def call_llm_vision(image_path: str, prompt: str) -> str:
    # Implement vision API call here
    return f"Vision analysis of {image_path} with prompt: {prompt}"

def call_llm_general(prompt: str) -> str:
    response = client.chat.completions.create(
        model="gpt-4",
        messages=[{"role": "user", "content": prompt}]
    )
    return response.choices[0].message.content

def call_llm_embeddings(texts: List[str]) -> List[List[float]]:
    response = client.embeddings.create(
        model="text-embedding-ada-002",
        input=texts
    )
    return [embedding.embedding for embedding in response.data]

def execute_sql_query(db_path: str, query: str) -> List[Dict[str, Any]]:
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    cursor.execute(query)
    columns = [col[0] for col in cursor.description]
    rows = cursor.fetchall()
    conn.close()
    return [dict(zip(columns, row)) for row in rows]

def run_shell_commands(commands: List[str]) -> List[str]:
    outputs = []
    for cmd in commands:
        result = subprocess.run(cmd, shell=True, capture_output=True, text=True)
        outputs.append(result.stdout.strip())
    return outputs

# Function calling definitions

functions = [
    {
        "name": "markdown_to_html",
        "description": "Convert Markdown text to HTML",
        "parameters": {
            "type": "object",
            "properties": {
                "markdown_text": {"type": "string", "description": "The Markdown text to convert"}
            },
            "required": ["markdown_text"]
        }
    },
    {
        "name": "call_llm_vision",
        "description": "Analyze an image using AI vision capabilities",
        "parameters": {
            "type": "object",
            "properties": {
                "image_path": {"type": "string", "description": "Path to the image file"},
                "prompt": {"type": "string", "description": "Prompt for image analysis"}
            },
            "required": ["image_path", "prompt"]
        }
    },
    {
        "name": "call_llm_general",
        "description": "Process a general text prompt using AI",
        "parameters": {
            "type": "object",
            "properties": {
                "prompt": {"type": "string", "description": "The text prompt to process"}
            },
            "required": ["prompt"]
        }
    },
    {
        "name": "call_llm_embeddings",
        "description": "Generate embeddings for a list of texts",
        "parameters": {
            "type": "object",
            "properties": {
                "texts": {"type": "array", "items": {"type": "string"}, "description": "List of texts to generate embeddings for"}
            },
            "required": ["texts"]
        }
    },
    {
        "name": "execute_sql_query",
        "description": "Execute a SQL query on a SQLite database",
        "parameters": {
            "type": "object",
            "properties": {
                "db_path": {"type": "string", "description": "Path to the SQLite database file"},
                "query": {"type": "string", "description": "SQL query to execute"}
            },
            "required": ["db_path", "query"]
        }
    },
    {
        "name": "run_shell_commands",
        "description": "Run a list of shell commands",
        "parameters": {
            "type": "object",
            "properties": {
                "commands": {"type": "array", "items": {"type": "string"}, "description": "List of shell commands to execute"}
            },
            "required": ["commands"]
        }
    }
]

def execute_function(function_name: str, arguments: Dict[str, Any]) -> Any:
    function_map = {
        "markdown_to_html": markdown_to_html,
        "call_llm_vision": call_llm_vision,
        "call_llm_general": call_llm_general,
        "call_llm_embeddings": call_llm_embeddings,
        "execute_sql_query": execute_sql_query,
        "run_shell_commands": run_shell_commands
    }
    
    if function_name not in function_map:
        raise ValueError(f"Unknown function: {function_name}")
    
    return function_map[function_name](**arguments)

@app.post("/run")
async def execute_task(task: str):
    messages = [
        {"role": "system", "content": "You are an AI assistant that helps with various tasks. Use the provided functions to complete the user's request."},
        {"role": "user", "content": task}
    ]
    
    while True:
        response = client.chat.completions.create(
            model="gpt-4",
            messages=messages,
            functions=functions,
            function_call="auto"
        )
        
        response_message = response.choices[0].message
        
        if response_message.function_call:
            function_name = response_message.function_call.name
            function_args = json.loads(response_message.function_call.arguments)
            
            function_response = execute_function(function_name, function_args)
            
            messages.append({
                "role": "function",
                "name": function_name,
                "content": str(function_response)
            })
        else:
            return {"result": response_message.content}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="127.0.0.1", port=8000)
