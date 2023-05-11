# 900510503:AAG5Xug_JEERhKlf7dpOpzxXcJIzlTbWX1M
# https://docs.aiogram.dev/en/latest/
from aiogram import Bot, Dispatcher, types
from aiogram.utils import executor
from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup
import subprocess
import json
import requests

API_TOKEN = '900510503:AAG5Xug_JEERhKlf7dpOpzxXcJIzlTbWX1M'

bot = Bot(token=API_TOKEN)
dp = Dispatcher(bot)

def getOpt() -> InlineKeyboardMarkup:
    opt = InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton('time', callback_data='time')]
    ])
    return opt

@dp.message_handler(commands=['start'])
async def cmd_start(message: types.Message) -> None:
    await message.reply('Тестирование асинхрона.\ntime - запускает бесконечный счётчик \n/info - выводит сообщение в телегу', reply_markup=getOpt())

@dp.callback_query_handler(text='time')
async def time(callback: types.CallbackQuery) -> None:
    print('time2')
    await callback.message.edit_text('time start callback')
    subprocess.Popen(['python', 'launch.py', '--nowebui', '--xformers'])

@dp.message_handler(commands=['info'])
async def start_info(message: types.Message):
    print('info')
    response = requests.get('http://127.0.0.1:7861/sdapi/v1/progress?skip_current_image=false', data=json.dumps(''))
    print(response.json())
    print(response.json()['eta_relative'])
    await bot.send_message(chat_id=message.from_user.id, text=response.json()['eta_relative'])
    await message.answer("Проверка асинхрона - info")

if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True)