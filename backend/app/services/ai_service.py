import base64

from google import genai

from app.core.config import GEMINI_API_KEY
from app.services.conversation_service import (
    add_message,
    get_history,
)


client = genai.Client(
    api_key=GEMINI_API_KEY
)




def ask_phohtaung(question: str) -> str:

    system_prompt = """
You are "ဖိုးထောင်", a friendly AI tutor for a Myanmar student.

LANGUAGE RULES:
- If the student asks in Myanmar language, answer entirely in Myanmar language.
- Do NOT answer in Khmer, Thai, Chinese, or any unrelated language.
- English technical terms are allowed when necessary.
- If you use an English technical term, explain its meaning in Myanmar.
- Never invent meanings for words.
- Carefully understand the student's exact question before answering.
- Give accurate, simple, student-friendly explanations.
- Answer directly and avoid unnecessary complicated wording.

Your name is ဖိုးထောင်.
"""

    # User message ကို memory ထဲသိမ်း
    add_message("user", question)

    history = get_history()

    contents = []

    for message in history:
        contents.append(
            f"{message['role']}: {message['content']}"
        )

    conversation = "\n".join(contents)

    response = client.models.generate_content(
        model="gemini-3.8-flash",
        contents=conversation,
        config={
            "system_instruction": system_prompt,
        },
    )

    answer = response.text

    # AI answer ကို memory ထဲသိမ်း
    add_message("assistant", answer)

    return answer


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