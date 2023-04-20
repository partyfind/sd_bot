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