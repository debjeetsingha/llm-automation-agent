from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import os
from dotenv import load_dotenv

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



@app.get("/")
def home():
    return {"hello":"world"}


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="127.0.0.1", port=8000)