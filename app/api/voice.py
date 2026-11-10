from fastapi import APIRouter, File, HTTPException, UploadFile
from fastapi.responses import Response
from pydantic import BaseModel, Field
from openai import OpenAI
from app.core.config import get_settings

router = APIRouter()

def client_and_settings():
    settings = get_settings()
    if not settings.openai_api_key: raise HTTPException(503, "OPENAI_API_KEY is not configured")
    return OpenAI(api_key=settings.openai_api_key), settings

@router.post("/voice/transcribe")
async def transcribe(file: UploadFile = File(...)):
    if not file.content_type or not file.content_type.startswith("audio/"):
        raise HTTPException(415, "Upload an audio file.")
    data = await file.read()
    if len(data) > 20 * 1024 * 1024: raise HTTPException(413, "Audio file exceeds 20 MB.")
    client, settings = client_and_settings()
    try:
        result = client.audio.transcriptions.create(
            model=settings.openai_transcribe_model,
            file=(file.filename or "audio.webm", data, file.content_type)
        )
        return {"text": result.text}
    except Exception as exc:
        raise HTTPException(502, "Transcription failed.") from exc

class SpeechRequest(BaseModel):
    text: str = Field(min_length=1, max_length=4000)
    voice: str = "alloy"

@router.post("/voice/speech")
def speech(payload: SpeechRequest):
    client, settings = client_and_settings()
    try:
        audio = client.audio.speech.create(
            model=settings.openai_speech_model, voice=payload.voice, input=payload.text
        )
        return Response(content=audio.content, media_type="audio/mpeg")
    except Exception as exc:
        raise HTTPException(502, "Speech generation failed.") from exc
