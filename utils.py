from pyrogram.types import Message

async def edit_or_reply(message: Message, text: str):
    try:
        await message.edit_text(text)
    except:
        await message.reply(text)