import os
from pyrogram import Client, filters
from pyrogram.types import Message
from utils import edit_or_reply

class BotManager:
    def __init__(self):
        self.api_id = int(os.getenv("API_ID"))
        self.api_hash = os.getenv("API_HASH")
        self.bot_token = os.getenv("BOT_TOKEN")
        self.app = Client("caption_editor_bot", api_id=self.api_id, api_hash=self.api_hash, bot_token=self.bot_token)
        self.group_id_dict = {}
        self.remove_caption_dict = {}

        @self.app.on_message(filters.command("start") & filters.private)
        async def start_command(client, message: Message):
            await edit_or_reply(message, "👋 Welcome to Caption Remover Bot!

Please send the **Group ID** where the caption needs to be modified.")
            self.group_id_dict[message.from_user.id] = "WAITING_GROUP_ID"

        @self.app.on_message(filters.text & filters.private)
        async def handle_text(client, message: Message):
            user_id = message.from_user.id
            if self.group_id_dict.get(user_id) == "WAITING_GROUP_ID":
                try:
                    group_id = int(message.text.strip())
                    self.group_id_dict[user_id] = group_id
                    await edit_or_reply(message, f"✅ Group ID set to `{group_id}`.

Now send the **text** that you want to remove from the caption.")
                except ValueError:
                    await edit_or_reply(message, "❌ Invalid Group ID. Please enter a valid numeric ID.")
            elif user_id in self.group_id_dict:
                self.remove_caption_dict[user_id] = message.text.strip()
                await edit_or_reply(message, f"✅ Text to remove set as: `{message.text}`

🛠️ All ready to process messages!")

    def run(self):
        self.app.run()