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
import logging
import asyncio

from aiogram import Bot, types
from aiogram.dispatcher import Dispatcher
from aiogram.types import ChatActions

# Задаем логгер для отслеживания ошибок
logging.basicConfig(level=logging.INFO)

# Инициализируем бота и диспетчер
bot = Bot(token='900510503:AAG5Xug_JEERhKlf7dpOpzxXcJIzlTbWX1M')
dp = Dispatcher(bot)


async def export_history(chat_id):
    # Задаем параметры запроса для получения истории сообщений
    offset = 0
    limit = 1000

    # Создаем файл для записи истории сообщений
    with open('history.txt', 'w', encoding='utf-8') as f:
        # Перед началом экспорта сообщений посылаем чату сигнал о начале загрузки
        await bot.send_chat_action(chat_id, ChatActions.TYPING)

        # Постепенно получаем все сообщения чата пачками по limit штук за раз
        while True:
            messages = await bot.get_chat_history(chat_id, limit=limit, offset=offset)

            # Если получено 0 сообщений - значит, история закончилась
            if not messages:
                break

            # Записываем полученные сообщения в файл и инкрементируем счетчик offset
            for message in messages:
                f.write(f'{message.date} {message.from_user.full_name} [{message.chat.title} ({message.chat.id})]: {message.text}\n')

            offset += limit

        # После завершения экспорта посылаем чату сигнал об окончании загрузки
        await bot.send_chat_action(chat_id, ChatActions.RECORD_VIDEO_NOTE)

        # Отправляем файл с историей сообщений в чат
        with open('history.txt', 'r', encoding='utf-8') as f:
            lines = f.readlines()
            for i in range(0, len(lines), 10):
                message = ''.join(lines[i:i+10])
                await bot.send_message(chat_id, message)

    # Удаляем файл истории сообщений
    os.remove('history.txt')


# Обрабатываем команду /export
@dp.message_handler(commands=['export'])
async def export_command_handler(message: types.Message):
    # Получаем ID чата, из которого отправлена команда
    chat_id = message.chat.id

    try:
        await export_history(chat_id)
        await message.answer('История сообщений чата успешно экспортирована в файл.')
    except Exception as e:
        await message.answer(f'Ошибка экспорта: {e}')


# Запускаем бота
if __name__ == '__main__':
    loop = asyncio.get_event_loop()
    loop.run_until_complete(dp.start_polling())
