import logging
from pyrogram import Client, filters # type: ignore
from plugins import gemini
import os

# 3. Memory: Disable verbose logging if not needed, or use a leaner format
logging.basicConfig(level=logging.WARNING) 
SESSION_STRING = os.getenv("SESSION_STRING")

app = Client(
    name="Kamski's Acount",
    api_hash=gemini.API_HASH, # type: ignore
    api_id=gemini.API_ID, # type: ignore
    session_string=SESSION_STRING, # type:ignore
    sleep_threshold=10,      # Optimization: Don't wait too long on flood waits
    in_memory=True           # Memory: Keep session in RAM to avoid slow Disk I/O
)

@app.on_message(filters.me & filters.command("ping", prefixes="."))
async def ping_handler(_, message):
    # 'ping' is the fastest way to check latency
    await message.edit_text("Pong!")

@app.on_message(filters.me & filters.command("search", prefixes="."))
async def search_handler(_, message): # _ used for something that we don't use since Pyrogram always gives us two arguments which is client and message.
    await message.edit_text("Thinking..")

    answer = await gemini.ask_gemini(message)

    await message.edit_text(answer)

# the fastest way to run modern Python scripts
if __name__ == "__main__":
    app.run()