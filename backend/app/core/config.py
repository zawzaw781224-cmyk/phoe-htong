import os
from dotenv import load_dotenv

load_dotenv()

GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")
FREETTS_API_KEY = os.getenv("FREETTS_API_KEY")
OPENROUTER_API_KEY = os.getenv("OPENROUTER_API_KEY")