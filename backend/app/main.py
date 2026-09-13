from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.api.tts import router as tts_router
from app.api.voice import router as voice_router
from app.api.chat import router as chat_router

app = FastAPI(title="ဖိုးထောင် AI Tutor")


app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://127.0.0.1:5500",
        "http://localhost:5500",
    ],
    allow_credentials=False,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(voice_router)
app.include_router(tts_router)
app.include_router(chat_router)

@app.get("/")
def root():
    return {
        "message": "ဖိုးထောင် AI Tutor API is running!"
    }