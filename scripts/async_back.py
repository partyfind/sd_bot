# 900510503:AAG5Xug_JEERhKlf7dpOpzxXcJIzlTbWX1M
# https://docs.aiogram.dev/en/latest/
from aiogram import Bot, Dispatcher, types
from aiogram.utils import executor
from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup
import subprocess

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
    print('time')
    await callback.message.edit_text('time start callback')
    process = subprocess.Popen(['python', 'time.py', '--nowebui', '--xformers'], stderr=subprocess.PIPE)
    while True:
        txt = process.stderr.readline().decode().strip()
        if txt == '':
            txt = 'Ждёмс'
        await callback.message.edit_text(txt)

@dp.message_handler(commands=['info'])
async def start_info(message: types.Message):
    await message.answer("Проверка асинхрона - info")

if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True)