from google import genai
from google.genai import types
import os

API_KEY = os.getenv("GEMINI_API_KEY")
API_ID = os.getenv("API_ID")
API_HASH = os.getenv("API_HASH")
MODEL_ID = "models/gemini-2.5-flash"

client = genai.Client(api_key=API_KEY)
GEN_CONFIG = types.GenerateContentConfig(temperature=0.7, max_output_tokens=800) # Having said this is the optimum output length for Telegram


async def ask_gemini(message):
    parts = message.text.split(None, 1)

    if len(parts) < 2:
        Usage =  "`Usage: .ask [query]`"
        return Usage
    
    prompts = parts[1]
    await message.edit_text("Asking..")

    try:
        response = await client.aio.models.generate_content(
            model=MODEL_ID,
            contents=prompts,
            config=GEN_CONFIG
        )

        return response.text
    except Exception as e:
        if "429" in str(e):
            return "**Error:** Gemini rate limit has reach! Please wait for a minute before asking again."
        elif "MESSAGE_TOO_LONG" in str(e):
            return "Response provided by Gemini is **too long**! Try again."
        return f"**Error: {str(e)}**"