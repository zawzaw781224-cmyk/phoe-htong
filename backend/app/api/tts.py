from fastapi import APIRouter
from fastapi.responses import Response
from pydantic import BaseModel

from app.services.tts_service import generate_speech

router = APIRouter()


class TTSRequest(BaseModel):
    text: str


@router.post("/tts")
def tts(request: TTSRequest):

    audio = generate_speech(request.text)

    return Response(
        content=audio,
        media_type="audio/mpeg"
    )