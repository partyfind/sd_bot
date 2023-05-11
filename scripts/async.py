# 900510503:AAG5Xug_JEERhKlf7dpOpzxXcJIzlTbWX1M
# https://docs.aiogram.dev/en/latest/
from aiogram import Bot, Dispatcher, types
from aiogram.utils import executor
import asyncio
from datetime import datetime

API_TOKEN = '900510503:AAG5Xug_JEERhKlf7dpOpzxXcJIzlTbWX1M'

bot = Bot(token=API_TOKEN)
dp = Dispatcher(bot)

@dp.message_handler(commands=['start'])
async def cmd_start(message: types.Message) -> None:
    await message.reply('Тестирование асинхрона.\n/time - запускает бесконечный счётчик \n/info - выводит сообщение в телегу')

async def get_time():
    while True:
        await asyncio.sleep(2)
        time = datetime.now().strftime("%H:%M:%S")
        print(f"Этот цикл продолжится бесконечно2! {time}")

@dp.message_handler(commands=['time'])
async def start_time(message: types.Message):
    await message.answer("Time started")
    asyncio.create_task(get_time())

@dp.message_handler(commands=['info'])
async def start_info(message: types.Message):
    await message.answer("Проверка асинхрона - info")

if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True)