import os
import base64
import mimetypes
from dotenv import load_dotenv
from openai import OpenAI
from typing import Dict, Any, Optional

load_dotenv(".env")

AIPROXY_TOKEN = os.getenv("AIPROXY_TOKEN")
API_BASE_URL = "https://aiproxy.sanand.workers.dev/openai/v1"

if not AIPROXY_TOKEN:
    raise ValueError("Missing AIPROXY_TOKEN in .env file")

def encode_image(image_path: str) -> Optional[str]:
    """Encodes an image in base64 and detects its MIME type."""
    try:
        mime_type, _ = mimetypes.guess_type(image_path)
        if not mime_type or not mime_type.startswith("image/"):
            return None  # Unsupported file format

        with open(image_path, "rb") as image_file:
            base64_image = base64.b64encode(image_file.read()).decode("utf-8")
        return f"data:{mime_type};base64,{base64_image}"
    except Exception:
        return None

def call_llm(prompt: str, image_path: Optional[str] = None) -> str:
    """
    Calls OpenAI's API with a given prompt.
    If an image is provided, it encodes the image in base64 before sending.
    """

    tool_client = OpenAI(api_key=AIPROXY_TOKEN, base_url=API_BASE_URL)
    sys_prompt = "You are a tool inside an AI agent. Your job is to assist the agent in executing tasks efficiently."

    messages = [{"role": "system", "content": sys_prompt}, {"role": "user", "content": prompt}]
    
    if image_path:
        image_data = encode_image(image_path)
        if not image_data:
            return "Error: Unsupported or invalid image file."

        messages.append({
            "role": "user",
            "content": [
                {"type": "text", "text": prompt},
                {"type": "image_url", "image_url": image_data},
            ],
        })

    try:
        response = tool_client.chat.completions.create(
            model="gpt-4o-mini",
            messages=messages
        )
        return {"response": response.choices[0].message.content }
    except Exception as e:
        return {"response":  f"Error: {str(e)}"}




