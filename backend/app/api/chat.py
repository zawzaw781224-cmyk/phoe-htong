from fastapi import APIRouter
from pydantic import BaseModel

from app.services.ai_service import ask_phohtaung


router = APIRouter()


class ChatRequest(BaseModel):
    message: str


@router.post("/chat")
def chat(request: ChatRequest):

    answer = ask_phohtaung(request.message)

    return {
        "answer": answer
    }