# tts 服务
from pathlib import Path
import openai
import uuid

OUTPUT_DIR = Path("backend/static/audio")
OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

def call_tts(text: str) -> str:
    file_name = f"{uuid.uuid4().hex}.mp3"
    file_path = OUTPUT_DIR / file_name

    with openai.audio.speech.with_streaming_response.create(
        model="gpt-4o-mini-tts",
        voice="alloy",
        input=text
    ) as response:
        response.stream_to_file(file_path)

    return f"http://127.0.0.1:8000/static/audio/{file_name}"

