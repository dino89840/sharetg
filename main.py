import os
import random
import asyncio
from pyrogram import Client

# Railway Variables မှ အချက်အလက်များကို ယူမည်
API_ID = int(os.getenv("API_ID"))
API_HASH = os.getenv("API_HASH")
BOT_TOKEN = os.getenv("BOT_TOKEN")
SOURCE_CHANNEL = os.getenv("SOURCE_CHANNEL") # ဥပမာ- -100...
TARGET_GROUP = os.getenv("TARGET_GROUP")     # ဥပမာ- @groupname
INTERVAL = int(os.getenv("INTERVAL", 3600))  # စက္ကန့်အလိုက် (Default: ၁ နာရီ)

app = Client("my_bot", api_id=API_ID, api_hash=API_HASH, bot_token=BOT_TOKEN)

async def auto_share():
    async with app:
        while True:
            try:
                # Channel ထဲက နောက်ဆုံး message ၅၀၀ ထဲက ဗီဒီယိုတွေကို ရှာမယ်
                video_ids = []
                async for message in app.get_chat_history(SOURCE_CHANNEL, limit=500):
                    if message.video:
                        video_ids.append(message.id)
                
                if video_ids:
                    random_id = random.choice(video_ids)
                    # Group ထဲကို Copy ပို့မယ်
                    await app.copy_message(
                        chat_id=TARGET_GROUP,
                        from_chat_id=SOURCE_CHANNEL,
                        message_id=random_id
                    )
                    print(f"Success: Shared video {random_id}")
                
                await asyncio.sleep(INTERVAL) # သတ်မှတ်ထားတဲ့ အချိန်စောင့်မယ်
            except Exception as e:
                print(f"Error: {e}")
                await asyncio.sleep(60) # Error တက်ရင် ၁ မိနစ်နားပြီး ပြန်လုပ်မယ်

if __name__ == "__main__":
    app.run(auto_share())
