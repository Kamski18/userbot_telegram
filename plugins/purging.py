import asyncio

async def purge(client, message):
    if not message.reply_to_message:
        await message.edit_text("__Reply to a message!__")
        return
    
    for i in range(message.reply_to_message.id, message.id, 100):
        await client.delete_messages(chat_id=message.chat.id, message_ids=list(range(i + 100, message.id))) # type: ignore

        await message.edit_text("__purge!, this message will auto delete in 5 seconds__")
        await asyncio.sleep(5)
        await message.delete()