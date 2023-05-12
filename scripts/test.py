import subprocess
import requests
import time
process = subprocess.Popen(['python', 'launch.py', '--nowebui', '--xformers'])
payload = {
    "prompt": "cat in car",
    "steps": 5
}
print(8)
n = 0
url = 'http://127.0.0.1:7861/docs'
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
print(24)
response = requests.post(url='http://127.0.0.1:7861/sdapi/v1/txt2img', json=payload)
print(response.json()['miages'][0])















import base64
import io
import requests
from PIL import Image
from telegram import Update, CallbackQuery
from telegram.ext import Updater, CallbackContext

# функция для конвертации base64 в фото
def convert_base64_to_photo(base64_string):
    image_data = base64.b64decode(base64_string)
    image = Image.open(io.BytesIO(image_data))
    return image

# функция для отправки фото в боте телеграм
def send_photo(update: Update, context: CallbackContext, photo):
    chat_id = update.callback_query.message.chat_id
    context.bot.send_photo(chat_id=chat_id, photo=photo)

# пример использования
if __name__ == '__main__':
    updater = Updater(token=YOUR_BOT_TOKEN, use_context=True)

    def callback_handler(update: Update, context: CallbackContext):
        # получаем base64 из атрибута data callback-запроса
        base64_string = update.callback_query.data
        # конвертируем base64 в фото
        photo = convert_base64_to_photo(base64_string)
        # отправляем фото в боте телеграм
        send_photo(update, context, photo=photo)

    updater.dispatcher.add_handler(CallbackQueryHandler(callback_handler))
    updater.start_polling()
    updater.idle()