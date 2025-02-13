from fastapi import FastAPI, HTTPException, Response
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from openai import OpenAI
import os
from dotenv import load_dotenv
from pathlib import Path
import subprocess
import json
from typing import Dict, Any, Optional

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

@app.get("/")
def home():
    return {"hello": "world"}

@app.get("/read")
async def read_file(path: str):
    file_path = Path("/data") / Path(path).name  # Ensuring correct file path
    if not file_path.is_file():
        return Response(status_code=404)
    try:
        with file_path.open("r", encoding="utf-8") as f:
            return Response(content=f.read(), media_type="text/plain")
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error reading file: {str(e)}")
    
if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="127.0.0.1", port=8000)
