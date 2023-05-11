# 900510503:AAG5Xug_JEERhKlf7dpOpzxXcJIzlTbWX1M
# https://docs.aiogram.dev/en/latest/
from aiogram import Bot, Dispatcher, types
from aiogram.utils import executor
from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup
import subprocess
import json
import requests
import time

API_TOKEN = '900510503:AAG5Xug_JEERhKlf7dpOpzxXcJIzlTbWX1M'

bot = Bot(token=API_TOKEN)
dp = Dispatcher(bot)

def getOpt() -> InlineKeyboardMarkup:
    opt = InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton('sd_on', callback_data='sd_on'),
         InlineKeyboardButton('gen', callback_data='gen')]
    ])
    return opt

@dp.message_handler(commands=['help'])
@dp.message_handler(commands=['start'])
async def cmd_start(message: types.Message) -> None:
    print('start')
    await message.reply('Тестирование асинхрона.\n/help', reply_markup=getOpt())

@dp.message_handler(commands=['opt'])
async def opt(message: types.Message) -> None:
    print('opt')
    await message.reply('Опции', reply_markup=getOpt())

@dp.callback_query_handler(text='sd_on')
async def sd_on(callback: types.CallbackQuery) -> None:
    print('sd_on')
    #subprocess.Popen(['python', 'launch.py', '--nowebui', '--xformers', '--share']) #, stderr=subprocess.PIPE, stdout=subprocess.PIPE
    print(38)
    try:
        output = subprocess.Popen(['python', 'launch.py', '--nowebui', '--xformers'], text=True) #, stderr=subprocess.PIPE, stdout=subprocess.PIPE
        print("stdout:", output.stdout)
        print("stderr:", output.stderr)
        #print(f"Pulled changes for repository in :\n{output.decode('utf-8').strip()}\n")
    except subprocess.CalledProcessError as e:
        print("e:", e)
        #print(f"Couldn't perform 'git pull' on repository in :\n{e.output.decode('utf-8').strip()}\n")
    #print('stdout = '+process.stdout.readline().decode().strip())
    #print('stderr = '+process.stderr.readline().decode().strip())

@dp.callback_query_handler(text='gen')
async def gen(callback: types.CallbackQuery) -> None:
    print('gen')
    response = requests.get('http://127.0.0.1:7861/sdapi/v1/progress?skip_current_image=false', data=json.dumps(''))
    e = response.json()['eta_relative']
    while e > 0:
        response = requests.get('http://127.0.0.1:7861/sdapi/v1/progress?skip_current_image=false', data=json.dumps(''))
        e = round(response.json()['eta_relative'], 1)
        time.sleep(2)
        await callback.message.edit_text(e, reply_markup=getOpt())
    await callback.message.edit_text('Готово', reply_markup=getOpt())


if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True)