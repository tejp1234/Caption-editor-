import os
from pyrogram import Client, filters
from pyrogram.types import Message
from utils import edit_or_reply  # Make sure this exists and works

api_id = int(os.getenv("API_ID"))
api_hash = os.getenv("API_HASH")
bot_token = os.getenv("BOT_TOKEN")

app = Client("caption_editor_bot", api_id=api_id, api_hash=api_hash, bot_token=bot_token)

group_id_dict = {}
remove_caption_dict = {}

@app.on_message(filters.command("start") & filters.private)
async def start_command(client, message: Message):
    await edit_or_reply(message, "👋 Welcome to Caption Remover Bot!\n\nPlease send the **Group ID** where the caption needs to be modified.")
    group_id_dict[message.from_user.id] = "WAITING_GROUP_ID"

@app.on_message(filters.text & filters.private)
async def handle_text(client, message: Message):
    user_id = message.from_user.id
    if group_id_dict.get(user_id) == "WAITING_GROUP_ID":
        try:
            group_id = int(message.text.strip())
            group_id_dict[user_id] = group_id
            await edit_or_reply(message, f"✅ Group ID set to `{group_id}`.\n\nNow send the **text** that you want to remove from the caption.")
        except ValueError:
            await edit_or_reply(message, "❌ Invalid Group ID. Please enter a valid numeric ID.")
    elif user_id in group_id_dict:
        remove_caption_dict[user_id] = message.text.strip()
        await edit_or_reply(message, f"✅ Text to remove set as: `{message.text}`\n\n🛠️ All ready to process messages!")

if __name__ == "__main__":
    app.run()
