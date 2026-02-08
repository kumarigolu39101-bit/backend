from fastapi import FastAPI
from pydantic import BaseModel
import os
import requests

app = FastAPI()

class ChatRequest(BaseModel):
    message: str

@app.get("/")
def home():
    return {"status": "AI backend running"}

@app.post("/chat")
def chat(req: ChatRequest):
    api_key = os.getenv("OPENAI_API_KEY")

    if not api_key:
        return {"error": "API key not set"}

    headers = {
        "Authorization": f"Bearer {api_key}",
        "Content-Type": "application/json"
    }

    data = {
        "model": "gpt-4o-mini",
        "messages": [
            {"role": "user", "content": req.message}
        ]
    }

    r = requests.post(
        "https://api.openai.com/v1/chat/completions",
        headers=headers,
        json=data
    )

    reply = r.json()["choices"][0]["message"]["content"]
    return {"reply": reply}
