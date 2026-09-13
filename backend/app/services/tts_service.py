import asyncio
import os
import tempfile

import edge_tts


VOICE = "my-MM-ThihaNeural"


def generate_speech(text: str) -> bytes:

    async def generate(output_file):

        communicate = edge_tts.Communicate(
            text,
            VOICE
        )

        await communicate.save(output_file)

    with tempfile.NamedTemporaryFile(
        suffix=".mp3",
        delete=False
    ) as temp_file:

        output_file = temp_file.name

    try:

        asyncio.run(generate(output_file))

        with open(output_file, "rb") as f:
            audio_data = f.read()

        return audio_data

    finally:

        if os.path.exists(output_file):
            os.remove(output_file)