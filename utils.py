# utils.py
from pyrogram.types import Message

async def edit_or_reply(message: Message, text: str):
    if message.from_user:
        if message.reply_to_message:
            await message.reply(text)
        else:
            await message.reply(text)
