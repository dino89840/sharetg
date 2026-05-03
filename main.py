import os
import random
import asyncio
from pyrogram import Client

# Railway Variables မှ အချက်အလက်များကို ယူမည်
API_ID = int(os.getenv("API_ID"))
API_HASH = os.getenv("API_HASH")
BOT_TOKEN = os.getenv("BOT_TOKEN")
SOURCE_CHANNEL = os.getenv("SOURCE_CHANNEL") # ဥပမာ- -1002395717312
TARGET_GROUP = os.getenv("TARGET_GROUP")     # ဥပမာ- bluetvpro68
# အချိန်ကို ၁ မိနစ် (60 စက္ကန့်) အဖြစ် တိုက်ရိုက်သတ်မှတ်ထားပါသည်
INTERVAL = 60 

app = Client("my_bot", api_id=API_ID, api_hash=API_HASH, bot_token=BOT_TOKEN)

async def auto_share():
    async with app:
        print("Bot စတင်အလုပ်လုပ်နေပါပြီ...")
        while True:
            try:
                # Channel ထဲက နောက်ဆုံး message ၅၀၀ ထဲက ဗီဒီယိုတွေကို ရှာမယ်
                video_messages = []
                async for message in app.get_chat_history(SOURCE_CHANNEL, limit=500):
                    if message.video:
                        video_messages.append(message.id)
                
                if video_messages:
                    random_id = random.choice(video_messages)
                    # copy_message သုံးခြင်းဖြင့် caption ပါ တစ်ပါတည်းပါလာမည်
                    await app.copy_message(
                        chat_id=TARGET_GROUP,
                        from_chat_id=SOURCE_CHANNEL,
                        message_id=random_id
                    )
                    print(f"Success: Shared video ID {random_id}")
                else:
                    print("Channel ထဲတွင် ဗီဒီယို ရှာမတွေ့ပါ။")
                
                # ၁ မိနစ် စောင့်ဆိုင်းခြင်း
                await asyncio.sleep(INTERVAL) 
            except Exception as e:
                print(f"Error: {e}")
                # Error တစ်ခုခုတက်လျှင် ခေတ္တနားပြီး ပြန်ကြိုးစားမည်
                await asyncio.sleep(10)

if __name__ == "__main__":
    app.run(auto_share())
