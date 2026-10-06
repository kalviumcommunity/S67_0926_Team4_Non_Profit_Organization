import os
from typing import Optional

from dotenv import load_dotenv
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import requests

load_dotenv(os.path.join(os.path.dirname(__file__), "..", ".env"))

app = FastAPI(title="OpenRouter Backend")


class ChatRequest(BaseModel):
    message: str
    model: str = "openai/gpt-4o-mini"
    system_prompt: str = "You are a helpful assistant."


def get_openrouter_key() -> Optional[str]:
    """Support the different key names commonly used in local .env files."""
    candidates = [
        "OPENROUTER_API_KEY",
        "OPEN_ROUTER_API_KEY",
        "Open_router_API_KEY",
        "OPENROUTER_KEY",
    ]

    for key in candidates:
        value = os.getenv(key)
        if value and value.strip():
            return value.strip()
    return None


@app.get("/")
def root():
    return {"message": "OpenRouter backend is running."}


@app.get("/health")
def health():
    return {"status": "ok"}


@app.post("/ask")
def ask_question(payload: ChatRequest):
    api_key = get_openrouter_key()
    if not api_key:
        raise HTTPException(
            status_code=500,
            detail="OpenRouter API key not found. Add OPENROUTER_API_KEY or Open_router_API_KEY in your .env file.",
        )

    messages = []
    if payload.system_prompt:
        messages.append({"role": "system", "content": payload.system_prompt})
    messages.append({"role": "user", "content": payload.message})

    response = requests.post(
        "https://openrouter.ai/api/v1/chat/completions",
        headers={
            "Authorization": f"Bearer {api_key}",
            "Content-Type": "application/json",
            "HTTP-Referer": "http://localhost:8000",
            "X-Title": "FOLIO Backend",
        },
        json={
            "model": payload.model,
            "messages": messages,
            "temperature": 0.7,
        },
        timeout=60,
    )

    if response.status_code != 200:
        try:
            error_text = response.json()
        except ValueError:
            error_text = response.text
        raise HTTPException(status_code=response.status_code, detail=f"OpenRouter error: {error_text}")

    data = response.json()
    try:
        answer = data["choices"][0]["message"]["content"]
    except (KeyError, IndexError, TypeError):
        raise HTTPException(status_code=500, detail=f"Unexpected OpenRouter response: {data}")

    return {
        "answer": answer,
        "model": payload.model,
    }


if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host="0.0.0.0", port=8000)
