import subprocess
import time
from aiogram import Bot, Dispatcher, types
from aiogram.utils import executor

bot_token = '5815882861:AAHVGTfEfozTaU0yRHJEEaYv7gSi4Ag_WBw'  # замените '<TOKEN>' на ваш токен
bot = Bot(token=bot_token)
dp = Dispatcher(bot)


async def send_error_message(chat_id, error_message):
    try:
        await bot.send_message(chat_id, f'Ошибка: {error_message}')
    except Exception as e:
        print(f"Ошибка отправки сообщения в Telegram: {e}")


async def main_loop(chat_id):
    # запускаем скрипт и перехватываем его stderr
    process = subprocess.Popen(['python', 'launch.py'], stderr=subprocess.PIPE)

    while True:
        error_message = process.stderr.readline().decode().strip()
        if error_message:
            print(error_message)  # выводим ошибку в консоль
            await send_error_message(chat_id, error_message)  # отправляем ошибку в Telegram


async def start_bot(app):
    await bot.send_message('125011869', 'Бот запущен')

    try:
        while True:
            await main_loop('125011869')  # замените '<CHAT_ID>' на ID вашего чата с ботом
            time.sleep(1)
    except Exception as e:
        print(f"Ошибка запуска бота или исключение: {e}")


if __name__ == '__main__':
    executor.start_polling(dp, on_startup=start_bot)
#___________________________
from googletrans import Translator

translator = Translator()
result = translator.translate("Проверка написания. Длинный текст про экспорт справочников. Нужно выгрузить солнечный ZIP, потом ещё что-то!", src='ru', dest='en')
print(result.text)
















#___________________________________________
import logging
import subprocess
import requests
import base64
import json
import os
from aiogram import Bot, types
from aiogram.dispatcher import Dispatcher
from aiogram.utils import executor

# настройка логирования
logging.basicConfig(filename='log.csv', level=logging.ERROR, format='%(asctime)s %(levelname)s %(message)s')

# создание бота и диспетчера
bot = Bot(token='5815882861:AAHVGTfEfozTaU0yRHJEEaYv7gSi4Ag_WBw')
dp = Dispatcher(bot)

# команда /start
@dp.message_handler(commands=['start'])
async def start_command(message: types.Message):
    keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)
    buttons = ["Launch", "Stop"]
    keyboard.add(*buttons)
    await message.answer("Hello! I can help you manage the launch of the API. Please select an option:", reply_markup=keyboard)

# кнопка "Запустить"
@dp.message_handler(lambda message: message.text == "Launch")
async def launch_command(message: types.Message):
    try:
        # запуск процесса
        print('Launch')
        process = subprocess.Popen(['python', 'launch.py', '--nowebui', '--xformers'], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        output, error = process.communicate()
        print(34)
        # проверка наличия ошибок
        if error:
            logging.error(error)
            await message.answer("Error occurred during launch", reply_markup=types.ReplyKeyboardRemove())
        else:
            await message.answer("API launched successfully", reply_markup=types.ReplyKeyboardRemove())

    except Exception as e:
        logging.error(str(e))
        await message.answer('Error occurred: ' + str(e), reply_markup=types.ReplyKeyboardRemove())

# кнопка "Остановить"
@dp.message_handler(lambda message: message.text == "Stop")
async def stop_command(message: types.Message):
    try:
        # остановка процесса
        subprocess.Popen(["pkill", "-f", "launch.py"])
        await message.answer("API stopped successfully", reply_markup=types.ReplyKeyboardRemove())

    except Exception as e:
        logging.error(str(e))
        await message.answer('Error occurred: ' + str(e), reply_markup=types.ReplyKeyboardRemove())

# обработка сообщений с фото
@dp.message_handler(content_types=['photo'])
async def handle_photo(message: types.Message):
    try:
        # загрузка фото
        file_id = message.photo[-1].file_id
        file = await message.bot.get_file(file_id)
        file_data = await file.download()

        # получение base64-кодированного изображения с API
        with open(file_data, "rb") as image_file:
            encoded_string = base64.b64encode(image_file.read())

        # сохранение изображения в папке img
        img_directory = 'img'
        os.makedirs(img_directory, exist_ok=True)
        img_filename = f'{img_directory}/photo_{message.chat.id}.jpeg'
        with open(img_filename, 'wb') as f:
            f.write(base64.b64decode(encoded_string))

        await message.answer("Image saved successfully", reply_markup=types.ReplyKeyboardRemove())

    except Exception as e:
        logging.error(str(e))
        await message.answer('Error occurred: ' + str(e), reply_markup=types.ReplyKeyboardRemove())

# запуск бота
if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True)



______________________________
#900510503:AAG5Xug_JEERhKlf7dpOpzxXcJIzlTbWX1M
from telegram import Update
from telegram.ext import Updater, CommandHandler, CallbackContext
import time
import sys

# Токен вашего Telegram бота
TOKEN = "900510503:AAG5Xug_JEERhKlf7dpOpzxXcJIzlTbWX1M"

# ID чата, куда будут отправляться сообщения
CHAT_ID = "125011869"

# Функция обработчик команды старта
def start(update: Update, context: CallbackContext):
    # Отправляем сообщение со статусом "In progress"
    message = context.bot.send_message(chat_id=CHAT_ID, text="In progress...")
    # Запускаем длительный процесс
    for i in range(10):
        time.sleep(1)  # Длительный процесс
        # Обновляем сообщение с прогрессом выполнения
        context.bot.edit_message_text(chat_id=CHAT_ID,
                                      message_id=message.message_id,
                                      text=f"Выполнено: {i+1}/10")
    # Отправляем сообщение с результатом выполнения
    context.bot.edit_message_text(chat_id=CHAT_ID,
                                  message_id=message.message_id,
                                  text="Готово!")
    # Завершаем выполнение скрипта
    sys.exit()

def main():
    # Создаем объект updater и привязываем его к Telegram боту
    updater = Updater(TOKEN) #, use_context=True
    # Создаем диспетчер для регистрации обработчиков команд
    dispatcher = updater.dispatcher
    # Регистрируем обработчик команды старта
    dispatcher.add_handler(CommandHandler("start", start))
    # Запускаем бота
    updater.start_polling()
    # Ожидаем остановки бота
    updater.idle()

if __name__ == '__main__':
    main()

#__________
# 900510503:AAG5Xug_JEERhKlf7dpOpzxXcJIzlTbWX1M
import asyncio
import subprocess
import datetime
import aiogram
from aiogram import Bot, Dispatcher, types


# Токен вашего бота
TOKEN = '900510503:AAG5Xug_JEERhKlf7dpOpzxXcJIzlTbWX1M'

# Идентификатор вашего чата с ботом
CHAT_ID = '125011869'


# Создаем экземпляры бота и диспетчера
bot = Bot(token=TOKEN)
dp = Dispatcher(bot)


# Обработчик команды для вывода системного времени
@dp.message_handler(commands=['time'])
async def cmd_time(message: types.Message):
    print('cmd_time')
    # Получаем текущее системное время
    now = datetime.datetime.now()

    # Отправляем сообщение с временем в чат
    await message.answer(f"Текущее время: {now}")


async def main():
    print('main')
    # Запускаем скрипт launch.py
    process = await asyncio.create_subprocess_exec(
        'python', 'time.py',
        stdout=subprocess.PIPE, stderr=subprocess.PIPE
    )

    # Читаем вывод скрипта launch.py и отправляем его в чат
    print(process.stdout)
    print(subprocess.PIPE)
    asyncio.create_task(read_pipe(process.stdout, 'stdout'))

    # Запускаем скрипт sys.py
    process2 = await asyncio.create_subprocess_exec(
        'python', 'sys.py',
        stdout=subprocess.PIPE, stderr=subprocess.PIPE
    )

    # Читаем вывод скрипта sys.py и отправляем его в чат
    asyncio.create_task(read_pipe(process2.stdout, 'stderr'))

    # Ждем завершения процессов запущенных скриптов
    await process.wait()
    await process2.wait()


async def read_pipe(pipe, label):
    print('read_pipe')
    # Читаем строки из стандартного вывода скрипта
    while True:
        # Читаем строку из стандартного вывода скрипта
        line = await pipe.readline()

        # Если строка пустая, значит процесс завершился
        if line == b'':
            break

        # Декодируем строку в utf-8 и отправляем ее в чат
        output = line.decode('utf-8').strip()
        await bot.send_message(CHAT_ID, f'{label}: {output}')


if __name__ == '__main__':
    print('__name__')
    # Запускаем цикл событий бота и ожидаем завершения работы
    asyncio.run(main())
#___________________
from aiogram import Bot, Dispatcher, types, executor
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.dispatcher.filters import Command

BOT_TOKEN = '900510503:AAG5Xug_JEERhKlf7dpOpzxXcJIzlTbWX1M'
bot = Bot(token=BOT_TOKEN)
dp = Dispatcher(bot, storage=MemoryStorage())

# Обработка команды /start
@dp.message_handler(Command("start"))
async def cmd_start(message: types.Message):
    print('cmd_start')
    await message.answer('Вы ввели старт')

async def set_sd(user_id: int, sd: int):
    await dp.storage.set_data(user=user_id, data='sd', value=sd)

@dp.message_handler(Command("sdon"))
async def sdon(message: types.Message):
    print('sdon')
    await handle_start_command(message)
    await message.answer('Вы ввели sdon')


@dp.message_handler(Command("sdoff"))
async def sdoff(message: types.Message):
    print('sdoff')
    await handle_stop_command(message)
    await message.answer('Вы ввели sdoff')

@dp.message_handler(Command("stat"))
async def stat(message: types.Message):
    print('stat')
    stats = await dp.storage.get_data()
    await message.answer(stats)

async def handle_start_command(message):
    await set_sd(message.from_user.id, 1) # присваиваем значение 1 переменной SD

async def handle_stop_command(message):
    await set_sd(message.from_user.id, 0) # присваиваем значение 0 переменной SD

if __name__ == '__main__':
    # Запускаем бота
    executor.start_polling(dp, skip_updates=True)

#____________________
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
    asyncio.create_task(send_time(asyncio.create_task(bot.send_message(message.chat.id, "Текущее время:"))))
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

#___________________
import json
from aiogram import Bot, Dispatcher, types
from aiogram.dispatcher import filters
from aiogram.utils import executor
import json
from aiogram import Bot, Dispatcher, types
from aiogram.types import ParseMode
from aiogram.utils import executor
from aiogram.dispatcher.filters import Command

# Инициализация бота и диспетчера
API_TOKEN = '900510503:AAG5Xug_JEERhKlf7dpOpzxXcJIzlTbWX1M'
bot = Bot(token=API_TOKEN)
dp = Dispatcher(bot)

# JSON данные
data = {
    "enable_hr": False,
    "prompt": "",
    "seed": -1,
    "override_settings_restore_afterwards": -1,
    "subseed_strength": 0
}

# Команда /get_json для вывода списка параметров
@dp.message_handler(commands=['get_json'])
async def get_json(message: types.Message):
    json_list = [f"/{key} = {value}" for key, value in data.items()]
    json_str = '\n'.join(json_list)
    await message.answer(f"JSON параметры:\n{json_str}")

# Функция для проверки типа значения по ключу
def check_value(key, value):
    if isinstance(value, bool) and key != "enable_hr":
        return False
    elif isinstance(value, int) and key != "seed" and key != "override_settings_restore_afterwards" and key != "subseed_strength":
        return False
    elif isinstance(value, str) and key != "prompt":
        return False
    return True

# Обработка команд для изменения значений в JSON
@dp.message_handler(filters.Command(commands=['enable_hr', 'prompt', 'seed', 'override_settings_restore_afterwards', 'subseed_strength']))
async def handle_command(message: types.Message):
    command = message.get_command()
    print(command)
    key = command[1:]
    value = data[key]

    # Определение типа значения по ключу и вывод предложения для изменения
    if check_value(key, value):
        await message.answer(f"Вы ввели {command}, у неё значение {value}, какое новое значение?")
    else:
        await message.answer("Ошибка! Невозможно изменить значение данного параметра.")

# Обработка введенных значений для изменения JSON
@dp.message_handler(lambda message: True)
async def change_json(message: types.Message):
    print(message.get_command())
    command = message.get_command()
    key = command[1:]

    # Если сообщение не начинается с /
    if not command.startswith("/") or key not in data.keys():
        return

    # Определение типа введенного значения и запись в JSON
    value = message.text[len(command) + 1:]
    if value.lower() == "true":
        data[key] = True
    elif value.lower() == "false":
        data[key] = False
    elif value.isnumeric():
        data[key] = int(value)
    else:
        data[key] = value

    await message.answer(f"Значение {command} изменилось на {data[key]}")

# Запуск бота
if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True)
#___________________
@dp.message_handler(state=Form)
async def answer_handler(message: types.Message):
    # Получаем аргументы команды
    args = message.get_args()
    if args:
        # Если аргументы есть, выводим их
        print(args)
        await message.reply(f"Вы ввели '/text {args}'")
    else:
        # Если аргументов нет, выводим сообщение об ошибке
        await message.reply("/text пуст")