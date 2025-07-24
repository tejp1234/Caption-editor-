import asyncio
from telethon import TelegramClient
from telethon.tl.functions.messages import EditMessage
import os

API_ID = int(os.getenv("API_ID"))
API_HASH = os.getenv("API_HASH")
BOT_TOKEN = os.getenv("BOT_TOKEN")
GROUP_ID = int(os.getenv("GROUP_ID"))
REMOVE_TEXT = os.getenv("REMOVE_TEXT")

client = TelegramClient('bot_session', API_ID, API_HASH).start(bot_token=BOT_TOKEN)

async def remove_word_from_captions():
    async for message in client.iter_messages(GROUP_ID):
        if message.message and REMOVE_TEXT in message.message:
            new_caption = message.message.replace(REMOVE_TEXT, '').strip()
            try:
                await client(EditMessage(
                    peer=GROUP_ID,
                    id=message.id,
                    message=new_caption
                ))
                print(f"✅ Edited message ID: {message.id}")
            except Exception as e:
                print(f"❌ Error editing message {message.id}: {e}")

asyncio.run(remove_word_from_captions())
