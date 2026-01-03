import os
import logging
from pyrogram import Client, filters
from google import genai
from google.genai import types

# 1. Performance: Use environment variables for keys to avoid hardcoding 
# and potential memory leaks in larger apps
API_KEY = os.getenv("GEMINI_API_KEY")
API_ID = 29490495
API_HASH = "9eacf1316c4dd5911464a6037de8e49c"
MODEL_ID = "gemini-2.0-flash" # Use current stable fast model

# 2. Optimization: Initialize GenAI Client once globally
# Use the new Google GenAI SDK's async-native client structure
gemini_client = genai.Client(api_key=API_KEY)
GEN_CONFIG = types.GenerateContentConfig(temperature=0.7)

# 3. Memory: Disable verbose logging if not needed, or use a leaner format
logging.basicConfig(level=logging.WARNING) 

app = Client(
    name="My_account", 
    api_id=API_ID, 
    api_hash=API_HASH,
    sleep_threshold=10,      # Optimization: Don't wait too long on flood waits
    in_memory=True           # Memory: Keep session in RAM to avoid slow Disk I/O
)

@app.on_message(filters.me & filters.command("ping", prefixes="."))
async def ping_handler(_, message):
    # 'ping' is the fastest way to check latency
    await message.edit_text("Pong!")

@app.on_message(filters.me & filters.command("search", prefixes="."))
async def search_handler(_, message):
    # Optimization: split(None, 1) is slightly faster than split(' ', 1)
    parts = message.text.split(None, 1)
    
    if len(parts) < 2:
        await message.edit_text("`Usage: .search [query]`")
        return

    prompt = parts[1]
    await message.edit_text("`Asking...`")

    try:
        # Optimization: Inline the call to avoid extra function stack overhead
        response = await gemini_client.aio.models.generate_content(
            model=MODEL_ID,
            contents=prompt,
            config=GEN_CONFIG
        )
        # Use edit_text for slightly better performance than edit()
        await message.edit_text(response.text)
        
    except Exception as e:
        await message.edit_text(f"**Error:** `{e}`")

if __name__ == "__main__":
    # Fastest way to run on modern Python
    app.run()