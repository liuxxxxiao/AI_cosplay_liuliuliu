# app/services/ollama_service.py
import requests
from app.config import OLLAMA_API_URL, DEFAULT_MODEL

def call_ollama(prompt: str, model: str = None, stream: bool = False) -> str:
    payload = {
        "model": model or DEFAULT_MODEL,
        "prompt": prompt,
        "stream": stream
    }
    res = requests.post(OLLAMA_API_URL, json=payload)
    res.raise_for_status()
    return res.json().get("response", "").strip()

