from aiogram import Bot, Dispatcher, types
from aiogram.utils import executor
from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup
import subprocess
import time
import json
import requests
import asyncio
import base64
from datetime import datetime
import aiohttp

bot = Bot('900510503:AAG5Xug_JEERhKlf7dpOpzxXcJIzlTbWX1M')
dp = Dispatcher(bot)
process = None
sd = '❌'
local = 'http://127.0.0.1:7861'


# Обработчик команды /post1
@dp.message_handler(commands=['post1'])
async def post1(message: types.Message):
    print('post1')
    # Задаем JSON payload
    payload = {
        "prompt": "cat in car",
        "steps": 55
    }
    # Создаем сессию
    async with aiohttp.ClientSession() as session:
        # Отправляем POST-запрос к первому сервису
        await message.answer('post1')
        async with session.post("http://127.0.0.1:7861/sdapi/v1/txt2img", json=payload) as response:
            # Получаем ответ и выводим его
            response_json = await response.json()
            print(response_json)

# Обработчик команды /post2
@dp.message_handler(commands=['post2'])
async def post2(message: types.Message):
    print('post2')
    # Создаем сессию
    async with aiohttp.ClientSession() as session:
        # Отправляем POST-запрос ко второму сервису
        async with session.post("http://127.0.0.1:7861/sdapi/v1/skip") as response:
            # Получаем ответ и выводим его
            response_json = await response.json()
            print(response_json)
            await message.answer('post2')

async def send_request(url, payload):
    async with aiohttp.ClientSession() as session:
        async with session.post(url, payload) as response:
            return await response.text()

async def start_sd():
    global process
    if not process:
        print('start_process sd')
        process = subprocess.Popen(['python', 'launch.py', '--nowebui', '--xformers'])
        await asyncio.get_running_loop().run_in_executor(None, process.communicate)

# Обработчик команды /launch
@dp.message_handler(commands='launch')
async def launch_handler(message: types.Message):
    asyncio.create_task(start_sd(), name='launch')


@dp.message_handler(commands=['help'])
@dp.message_handler(commands=['start'])
async def cmd_start(message: types.Message) -> None:
    print('cmd_start')
    await message.reply('Это бот для локального завуска SD.\n/opt\n/gen\n/help', reply_markup=getStart())

# Стартовое меню
def getStart() -> InlineKeyboardMarkup:
    st = InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton('sd'+sd, callback_data='sd'),
         InlineKeyboardButton('opt',   callback_data='opt'),
         InlineKeyboardButton('gen',   callback_data='gen'),
         InlineKeyboardButton('help',  callback_data='help')]
    ])
    return st

# Вызов меню генераций
@dp.callback_query_handler(text='gen')
async def inl_gen(callback: types.CallbackQuery) -> None:
    print('inl_gen')
    await callback.message.edit_text('Виды генераций', reply_markup=getGen())

def getGen() -> InlineKeyboardMarkup:
    gen = InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton('gen1', callback_data='gen1'),
         InlineKeyboardButton('gen4', callback_data='gen4'),
         InlineKeyboardButton('gen10', callback_data='gen10'),
         InlineKeyboardButton('gen_hr', callback_data='gen_hr'),
         InlineKeyboardButton('gen_hr4', callback_data='gen_hr4')]
    ])
    return gen

@dp.callback_query_handler(text='gen1')
async def inl_gen1(callback: types.CallbackQuery) -> None:
    print('inl_gen1')
    payload = {
        "prompt": "cat in car",
        "steps": 25
    }
    #response = requests.post(url=local+'/sdapi/v1/txt2img', json=payload)
    response = await asyncio.gather(send_request(local+'/sdapi/v1/txt2img', payload), send_request('http://127.0.0.1:7861/sdapi/v1/skip', None))
    photo = base64.b64decode(response.json()['images'][0])
    await callback.message.answer_photo(photo, caption='Готово', reply_markup=getGen())

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
        #start_sd()
        asyncio.create_task(start_sd(), name='launch')
        sd = '⌛'
        await callback.message.edit_text('Запускаем SD', reply_markup=getStart())
        ping('start')
        sd = '✅'
        await callback.message.edit_text('SD запущена \n/opt\n/gen\n/help', reply_markup=getStart())
async def send_time(background_task: asyncio.Task):
    while True:
        current_time = datetime.now().strftime('%H:%M:%S')
        print(current_time)
        await asyncio.sleep(1)

# Пропустить картинку
@dp.message_handler(commands=['skip'])
async def cmd_skip(message: types.Message) -> None:
    print('cmd_skip')
    send_message = await bot.send_message(message.chat.id, 'skip')
    requests.get(local+'/sdapi/v1/skip')
    await send_message.edit_text('Готово', reply_markup=getStart())

# Проверка прогресса
@dp.message_handler(commands=['stat'])
async def cmd_stat(message: types.Message) -> None:
    #asyncio.create_task(send_time(asyncio.create_task(bot.send_message(message.chat.id, "Текущее время:"))))
    print('cmd_stat')
    send_message = await bot.send_message(message.chat.id, 'Картинка генерируется')
    response = requests.get(local+'/sdapi/v1/progress?skip_current_image=false', data=json.dumps(''))
    e = response.json()['eta_relative']
    while e > 0:
        response = requests.get(local+'/sdapi/v1/progress?skip_current_image=false', data=json.dumps(''))
        e = round(response.json()['eta_relative'], 1)
        time.sleep(2)
        await send_message.edit_text(e, reply_markup=getStart())
    await send_message.edit_text('Готово', reply_markup=getStart())
# Обработчик команды /stop
@dp.message_handler(commands='stop')
async def stop_handler(message: types.Message):
    global process
    if process:
        print('stop_process sd')
        process.terminate()
        process = None
    await message.answer('Фоновый скрипт остановлен')



# Обработчик команды /time
@dp.message_handler(commands='time')
async def time_handler(message: types.Message):
    # Выводим текущее системное время
    await message.answer(str(datetime.now()))

if __name__ == '__main__':
    executor.start_polling(dp)