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

process = None
sd = '❌'

def start_sd():
    global process
    if not process:
        print('start_process sd')
        try:
            process = subprocess.Popen(['python', 'launch.py', '--nowebui', '--xformers'])
            # TODO stderr, stdout выводить в сообщение телеграм
        except subprocess.CalledProcessError as e:
            print("e:", e)

def stop_sd():
    global process, sd
    if process:
        print('stop_process sd')
        process.terminate()
        process = None
        sd = '❌'

def getOpt() -> InlineKeyboardMarkup:
    opt = InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton('sd'+sd, callback_data='sd'),
         InlineKeyboardButton('gen', callback_data='gen')]
    ])
    return opt

def getStart() -> InlineKeyboardMarkup:
    opt = InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton('sd'+sd, callback_data='sd'),
         InlineKeyboardButton('gen', callback_data='gen')]
    ])
    return opt

def ping(status: str):
    n = 0
    url = 'http://127.0.0.1:7861/docs'
    if status == 'stop':
        while n == 200:
            time.sleep(3)
            try:
                r = requests.get(url, timeout=3)
                r.raise_for_status()
                n = r.status_code
                print(r.status_code)
            except requests.exceptions.HTTPError as errh:
                print("Http Error:", errh)
            except requests.exceptions.ConnectionError as errc:
                print("Error Connecting:", errc)
            except requests.exceptions.Timeout as errt:
                print("Timeout Error:", errt)
            except requests.exceptions.RequestException as err:
                print("OOps: Something Else", err)
        return True
    else:
        while n != 200:
            time.sleep(3)
            try:
                r = requests.get(url, timeout=3)
                r.raise_for_status()
                n = r.status_code
                print(r.status_code)
            except requests.exceptions.HTTPError as errh:
                print("Http Error:", errh)
            except requests.exceptions.ConnectionError as errc:
                print("Error Connecting:", errc)
            except requests.exceptions.Timeout as errt:
                print("Timeout Error:", errt)
            except requests.exceptions.RequestException as err:
                print("OOps: Something Else", err)
        return True

@dp.message_handler(commands=['help'])
@dp.message_handler(commands=['start'])
async def cmd_start(message: types.Message) -> None:
    print('start')
    await message.reply('Тестирование асинхрона.\n/help', reply_markup=getOpt())

@dp.message_handler(commands=['opt'])
async def opt(message: types.Message) -> None:
    print('opt')
    await message.reply('Опции', reply_markup=getOpt())

@dp.callback_query_handler(text='sd')
async def cmd_sd(callback: types.CallbackQuery) -> None:
    print('cmd_sd')
    global sd
    if sd == '✅':
        stop_sd()
        sd = '⌛'
        await callback.message.edit_text('Останавливаем SD', reply_markup=getOpt())
        ping('stop')
        sd = '❌'
        await callback.message.edit_text('SD остановлена', reply_markup=getOpt())
    else:
        start_sd()
        sd = '⌛'
        await callback.message.edit_text('Запускаем SD', reply_markup=getOpt())
        ping('start')
        sd = '✅'
        await callback.message.edit_text('SD запущена', reply_markup=getOpt())

@dp.message_handler(commands=['stop'])
async def cmd_stop(message: types.Message) -> None:
    print('cmd_stop')
    global sd
    stop_sd()
    sd = '⌛' # ?
    ping('stop')
    sd = '❌'
    await bot.send_message(chat_id=message.from_user.id, text='SD остановлена', reply_markup=getOpt())

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