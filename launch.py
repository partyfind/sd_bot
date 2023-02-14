import asyncio
from aiogram import Bot

BOT_TOKEN = "5815882861:AAHVGTfEfozTaU0yRHJEEaYv7gSi4Ag_WBw"

async def main():
    bot = Bot(token=BOT_TOKEN)

    try:
        me = await bot.get_me()
        print(f"🤖 Hello, I'm {me.first_name}.\nHave a nice Day!")
    finally:
        await bot.close()

asyncio.run(main())