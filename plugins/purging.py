import asyncio

async def purge(client, message):
    if not message.reply_to_message:
        await message.edit_text("__Reply to a message!__")
        return

    start_id = message.reply_to_message.id
    end_id = message.id

    ids = list(range(start_id, end_id))

    for i in range(0, len(ids), 100):
        await client.delete_messages(
            chat_id=message.chat.id,
            message_ids=ids[i:i + 100]
        )
        await asyncio.sleep(0.3)  # prevent floodwait

    status = await message.edit_text("__Purge completed. Auto deleting...__")
    await asyncio.sleep(5)
    await status.delete()
