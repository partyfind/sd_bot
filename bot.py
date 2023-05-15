# 900510503:AAG5Xug_JEERhKlf7dpOpzxXcJIzlTbWX1M
# https://docs.aiogram.dev/en/latest/
from aiogram import Bot, Dispatcher, types
from aiogram.utils import executor
from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup, Message, CallbackQuery
import subprocess
import time
import json
import requests
import asyncio
import base64
from datetime import datetime
import aiohttp
from typing import Union

API_TOKEN = '900510503:AAG5Xug_JEERhKlf7dpOpzxXcJIzlTbWX1M'

bot = Bot(token=API_TOKEN)
dp = Dispatcher(bot)

# -------- GLOBAL ----------

local = 'http://127.0.0.1:7861'
process = None
sd = '❌'

# -------- FUNCTIONS ----------

# Запуск SD через subprocess и запись в глобальную переменную process
def start_sd():
    global process
    if not process:
        print('start_process sd')
        try:
            process = subprocess.Popen(['python', 'launch.py', '--nowebui', '--xformers'])
            # TODO stderr, stdout выводить в сообщение телеграм
        except subprocess.CalledProcessError as e:
            print("e:", e)

# Остановка SD
def stop_sd():
    global process, sd
    if process:
        print('stop_process sd')
        process.terminate()
        process = None
        sd = '❌'

# Проверка связи до запущенной локальной SD с nowebui
def ping(status: str):
    n = 0
    url = local+'/docs'
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

# -------- MENU ----------
# Стартовое меню
def getStart(returnAll = 1) -> InlineKeyboardMarkup:
    keys = [InlineKeyboardButton('sd'+sd, callback_data='sd'),
            InlineKeyboardButton('opt',   callback_data='opt'),
            InlineKeyboardButton('skip',   callback_data='skip'),
            InlineKeyboardButton('gen',   callback_data='gen'),
            InlineKeyboardButton('help',  callback_data='help')]
    st = InlineKeyboardMarkup(inline_keyboard=[keys])
    if returnAll == 1:
        return st
    else:
        return keys

# Меню опций
def getOpt(returnAll = 1) -> InlineKeyboardMarkup:
    keys = [InlineKeyboardButton('scripts',  callback_data='scripts'),
            InlineKeyboardButton('settings', callback_data='settings'),
            InlineKeyboardButton('prompt',   callback_data='prompt')]
    opt = InlineKeyboardMarkup(inline_keyboard=[keys])
    if returnAll == 1:
        return opt
    else:
        return keys

# Меню генераций
def getGen(returnAll = 1) -> InlineKeyboardMarkup:
    keys = [InlineKeyboardButton('gen1', callback_data='gen1'),
            InlineKeyboardButton('gen4', callback_data='gen4'),
            InlineKeyboardButton('gen10', callback_data='gen10'),
            InlineKeyboardButton('gen_hr', callback_data='gen_hr'),
            InlineKeyboardButton('gen_hr4', callback_data='gen_hr4')]
    gen = InlineKeyboardMarkup(inline_keyboard=[keys])
    if returnAll == 1:
        return gen
    else:
        return keys

# -------- COMMANDS ----------
# start/help
@dp.message_handler(commands=['help'])
@dp.message_handler(commands=['start'])
async def cmd_start(message: types.Message) -> None:
    print('cmd_start')
    await message.reply('Это бот для локального завуска SD.\n/skip\n/opt\n/gen\n/help', reply_markup=getStart())

# Получить опции
@dp.message_handler(commands=['opt'])
async def cmd_opt(message: types.Message) -> None:
    print('cmd_opt')
    await message.reply('Опции', reply_markup=getOpt())

# Получить опции inline
@dp.callback_query_handler(text='opt')
async def inl_opt(callback: types.CallbackQuery) -> None:
    print('inl_opt')
    await callback.message.edit_text('Опции', reply_markup=getOpt())

# Получить опции inline
@dp.callback_query_handler(text='help')
async def inl_help(callback: types.CallbackQuery) -> None:
    print('inl_help')
    await callback.message.edit_text('Опции', reply_markup=getOpt())

# Запуск/Остановка SD. Завязываемся на глобальную иконку sd
@dp.callback_query_handler(text='sd')
async def inl_sd(callback: types.CallbackQuery) -> None:
    print('inl_sd')
    global sd
    if sd == '✅':
        stop_sd()
        sd = '⌛'
        await callback.message.edit_text('Останавливаем SD', reply_markup=getStart())
        ping('stop')
        sd = '❌'
        await callback.message.edit_text('SD остановлена \n/opt\n/gen\n/help', reply_markup=getStart())
    else:
        start_sd()
        sd = '⌛'
        await callback.message.edit_text('Запускаем SD', reply_markup=getStart())
        ping('start')
        sd = '✅'
        await callback.message.edit_text('SD запущена \n/opt\n/gen\n/help', reply_markup=getStart())

# Остановка SD по /stop
@dp.message_handler(commands=['stop'])
async def cmd_stop(message: types.Message) -> None:
    print('cmd_stop')
    global sd
    stop_sd()
    sd = '⌛' # ?
    ping('stop')
    sd = '❌'
    await bot.send_message(chat_id=message.from_user.id, text='SD остановлена', reply_markup=getOpt())

async def send_time(background_task: asyncio.Task):
    while True:
        current_time = datetime.now().strftime('%H:%M:%S')
        print(current_time)
        await asyncio.sleep(1)

# Проверка прогресса
@dp.message_handler(commands=['stat'])
async def cmd_stat(message: types.Message) -> None:
    asyncio.create_task(send_time(asyncio.create_task(bot.send_message(message.chat.id, "Текущее время:"))))
    print('cmd_stat')
    send_message = await bot.send_message(message.chat.id, 'Картинка генерируется')
    response = requests.get(local+'/sdapi/v1/progress?skip_current_image=false', data=json.dumps(''))
    e = response.json()['eta_relative']
    while e > 0:
        response = requests.get(local+'/sdapi/v1/progress?skip_current_image=false', data=json.dumps(''))
        e = round(response.json()['eta_relative'], 1)
        time.sleep(2)
        await send_message.edit_text(e, reply_markup=getOpt())
    await send_message.edit_text('Готово', reply_markup=getOpt())

# Вызов меню генераций getGen
@dp.message_handler(commands=["gen"])
@dp.callback_query_handler(text="gen")
async def inl_gen(message: Union[types.Message, types.CallbackQuery]) -> None:
    print([getGen(0), getOpt(0)])
    print('inl_gen')
    keyboard = InlineKeyboardMarkup(inline_keyboard=[getGen(0), getStart(0)])
    # Если команда /gen
    if hasattr(message, 'content_type'):
        await bot.send_message(chat_id=message.from_user.id, text='Виды генераций', reply_markup=keyboard)
    else:
        await bot.edit_message_text(
            chat_id=message.message.chat.id,
            message_id=message.message.message_id,
            text='Виды генераций',
            reply_markup=keyboard
        )

# Генерация одной картинки
@dp.callback_query_handler(text='gen1')
async def inl_gen1(callback: types.CallbackQuery) -> None:
    print('inl_gen1')
    # TODO проверка на включенность SD
    prompt = 'cat in cap'
    payload = {
        "prompt": prompt,
        "steps": 25
    }
    send_message = await bot.send_message(callback.message.chat.id, 'Картинка генерируется. Промпт: `'+prompt+'`', parse_mode='Markdown')
    #response = requests.post(url=local+'/sdapi/v1/txt2img', json=payload)

    # Создаем сессию
    async with aiohttp.ClientSession() as session:
        # Отправляем POST-запрос к первому сервису
        async with session.post(local+'/sdapi/v1/txt2img', json=payload) as response_txt2img:
            # Получаем ответ и выводим его
            response_json = await response_txt2img.json()
        photo = base64.b64decode(response_json['images'][0])
        await callback.message.answer_photo(photo, caption='Готово', reply_markup=getGen())

# Обработчик команды /skip
@dp.message_handler(commands=['skip'])
async def skip(message: types.Message):
    print('skip')
    # Создаем сессию
    async with aiohttp.ClientSession() as session:
        # Отправляем POST-запрос ко второму сервису
        async with session.post(local + '/sdapi/v1/skip') as response:
            # Получаем ответ и выводим его
            response_json = await response.json()
            print(response_json)
            await message.answer('skip')

# -------- BOT POLLING ----------
if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True)

# -------- COPYRIGHT ----------
# Мишген
# join https://t.me/mishgenai