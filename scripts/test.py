import subprocess
import requests
import time
import io
import base64
from PIL import Image
from aiogram import Bot, Dispatcher, types
from aiogram.utils import executor
from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup
import subprocess
import time
from PIL import Image, PngImagePlugin

API_TOKEN = '900510503:AAG5Xug_JEERhKlf7dpOpzxXcJIzlTbWX1M'

bot = Bot(token=API_TOKEN)
dp = Dispatcher(bot)

# функция для конвертации base64 в фото
def convert_base64_to_photo(base64_string):
    image_data = base64.b64decode(base64_string)
    image = Image.open(io.BytesIO(image_data))
    return image

@dp.message_handler(commands=['start'])
async def cmd_start(message: types.Message) -> None:
    print('cmd_start')
    process = subprocess.Popen(['python', 'launch.py', '--nowebui', '--xformers'])
    payload = {
        "prompt": "cat in car",
        "steps": 15
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
    #photo = convert_base64_to_photo(response.json()['images'][0])
    binary_image = base64.b64decode(response.json()['images'][0])
    await bot.send_photo(message.chat.id, binary_image)
    #await message.answer_photo(photo, caption="caption")


if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True)