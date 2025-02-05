from pydantic import BaseModel
from openai import OpenAI
import os
from dotenv import load_dotenv


load_dotenv(".env")
OPENAI_API_KEY = os.getenv("AIPROXY_TOKEN")  

client = OpenAI(
    api_key=OPENAI_API_KEY,
    base_url="https://aiproxy.sanand.workers.dev/openai/v1"
    )

class CalendarEvent(BaseModel):
    name: str
    date: str
    participants: list[str]

completion = client.beta.chat.completions.parse(
    model="gpt-4o-mini",
    messages=[
        {"role": "system", "content": "Extract the event information."},
        {"role": "user", "content": "Alice and Bob are going to a science fair on Friday."},
    ],
    response_format=CalendarEvent,
)

event = completion.choices[0].message.parsed
print(event)