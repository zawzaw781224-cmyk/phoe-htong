import base64
import requests

from google import genai

from app.core.config import (
    GEMINI_API_KEY,
    OPENROUTER_API_KEY,
)


# Gemini client — နောက်ပိုင်းပြန်သုံးနိုင်အောင်ထားမယ်
client = genai.Client(api_key=GEMINI_API_KEY)


OPENROUTER_URL = "https://openrouter.ai/api/v1/chat/completions"


def ask_phohtaung(question: str) -> str:
    response = requests.post(
        OPENROUTER_URL,
        headers={
            "Authorization": f"Bearer {OPENROUTER_API_KEY}",
            "Content-Type": "application/json",
        },
        json={
            "model": "google/gemma-4-31b-it:free",
            "messages": [
                {
    "role": "system",
    "content": """
You are "ဖိုးထောင်", a friendly AI tutor for a Myanmar student.

LANGUAGE RULES:
- If the student asks in Myanmar language, answer entirely in Myanmar language.
- Do NOT answer in Khmer, Thai, Chinese, or any unrelated language.
- English technical terms are allowed when necessary.
- If you use an English technical term, explain its meaning in Myanmar.
- Never invent meanings for words.
- Carefully understand the student's exact question before answering.
- If the student asks about "ဝက်ဘ်ဆိုက်", understand it as "website", not "brick".
- Give accurate, simple, student-friendly explanations.
- Answer directly and avoid unnecessary complicated wording.

Your name is ဖိုးထောင်.
"""
},
                {
                    "role": "user",
                    "content": question,
                },
            ],
        },
        timeout=60,
    )

    response.raise_for_status()

    data = response.json()

    return data["choices"][0]["message"]["content"]


def transcribe_audio(audio_bytes: bytes, mime_type: str) -> str:
    audio_base64 = base64.b64encode(audio_bytes).decode("utf-8")

    interaction = client.interactions.create(
        model="gemini-3.8-flash",
        input=[
            {
                "type": "text",
                "text": (
                    "Generate an accurate transcript of the speech "
                    "in this audio. Preserve Myanmar and English words as spoken."
                ),
            },
            {
                "type": "audio",
                "data": audio_base64,
                "mime_type": mime_type,
            },
        ],
    )

    return interaction.output_text