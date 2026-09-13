from fastapi import APIRouter, UploadFile, File

from app.services.ai_service import (
    transcribe_audio,
    ask_phohtaung,
)


router = APIRouter()


@router.post("/voice")
async def voice(file: UploadFile = File(...)):

    audio_data = await file.read()

    # 🎤 Audio → Text
    text = transcribe_audio(
        audio_data,
        file.content_type or "audio/webm"
    )

    # 🧠 Text → AI Answer
    answer = ask_phohtaung(text)

    return {
        "text": text,
        "answer": answer
    }