import base64
import time

from google import genai
from google.genai import types

from app.core.config import GEMINI_API_KEY
from app.services.conversation_service import (
    add_message,
    get_history,
)


# ==============================
# Gemini Client
# ==============================

client = genai.Client(
    api_key=GEMINI_API_KEY
)


# ==============================
# Ask Phoe Htung
# ==============================

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


    # ==============================
    # Build Conversation
    # ==============================

    # ဒီနေရာမှာ user message ကို
    # Gemini အောင်မြင်ပြီးမှ memory ထဲသိမ်းမယ်။
    history = get_history()

    contents = []

    for message in history:
        contents.append(
            f"{message['role']}: {message['content']}"
        )

    # လက်ရှိ user question ကို conversation ထဲထည့်
    contents.append(
        f"user: {question}"
    )

    conversation = "\n".join(contents)


    # ==============================
    # Gemini Request + Retry
    # ==============================

    max_retries = 3

    response = None

    for attempt in range(max_retries):

        try:

            print(
                f"🤖 Gemini request "
                f"(attempt {attempt + 1}/{max_retries})"
            )

            response = client.models.generate_content(
                model="gemini-3.8-flash",
                contents=conversation,
                config=types.GenerateContentConfig(
                    system_instruction=system_prompt,
                ),
            )

            print("✅ Gemini response ရပါပြီ")

            break


        except Exception as error:

            print(
                f"⚠️ Gemini request failed "
                f"(attempt {attempt + 1}/{max_retries})"
            )

            print(
                f"⚠️ Error: {error}"
            )


            # နောက်ဆုံး attempt ဖြစ်ရင်
            # error ကို backend ဆီပြန်ပို့
            if attempt == max_retries - 1:

                print(
                    "❌ Gemini request အားလုံး မအောင်မြင်ပါ"
                )

                raise


            # Retry မလုပ်ခင် 2 seconds စောင့်
            print(
                "⏳ 2 seconds စောင့်ပြီး retry လုပ်ပါမယ်..."
            )

            time.sleep(2)


    # ==============================
    # Get Answer
    # ==============================

    answer = response.text


    # ==============================
    # Save Conversation
    # ==============================

    # Gemini အောင်မြင်မှသာ
    # user + assistant ကို memory ထဲသိမ်းမယ်
    add_message(
        "user",
        question
    )

    add_message(
        "assistant",
        answer
    )


    return answer


# ==============================
# Audio → Text
# ==============================

def transcribe_audio(
    audio_bytes: bytes,
    mime_type: str
) -> str:

    audio_base64 = base64.b64encode(
        audio_bytes
    ).decode("utf-8")


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