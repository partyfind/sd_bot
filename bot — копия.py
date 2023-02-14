"""
This is a echo bot.
It echoes any incoming text messages.
"""
import json
import base64
import requests
import logging

from aiogram import Bot, Dispatcher, executor, types

API_TOKEN = '5815882861:AAHVGTfEfozTaU0yRHJEEaYv7gSi4Ag_WBw'

# Configure logging
logging.basicConfig(level=logging.INFO)

# Initialize bot and dispatcher
bot = Bot(token=API_TOKEN)
dp = Dispatcher(bot)

def submit_post(url: str, data: dict):
    """
    Submit a POST request to the given URL with the given data.
    """
    return requests.post(url, data=json.dumps(data))
    
def save_encoded_image(b64_image: str, output_path: str):
    """
    Save the given image to the given output path.
    """
    with open(output_path, "wb") as image_file:
        image_file.write(base64.b64decode(b64_image))

@dp.message_handler(commands=['start', 'help'])
async def send_welcome(message: types.Message):
    """
    This handler will be called when user sends `/start` or `/help` command
    """
    await message.reply("Hi!\nI'm EchoBot!\nPowered by aiogram.")


@dp.message_handler(commands=['cat', 'test'])
async def cats(message: types.Message):
    txt2img_url = 'http://127.0.0.1:7861/sdapi/v1/txt2img'
    data = {'prompt': 'a dog wearing a glasses', 'steps':'5'}
    response = submit_post(txt2img_url, data)
    save_encoded_image(response.json()['images'][0], 'dog.png')
    with open('dog.png', 'rb') as photo:
        await message.reply_photo(photo, caption='Cats are here 😺')

"""
@dp.message_handler()
async def echo(message: types.Message):
    # old style:
    # await bot.send_message(message.chat.id, message.text)

    await message.answer(message.text)
"""

@dp.message_handler()
async def echo(message: types.Message):
    # old style:
    # await bot.send_message(message.chat.id, message.text)
    txt2img_url = 'http://127.0.0.1:7861/sdapi/v1/txt2img'
    data = {
    'prompt': message.text, 
    'steps':'30',
    'sd_model_checkpoint':'deliberate_v11.ckpt [10a699c0f3]'
    }
    response = submit_post(txt2img_url, data)
    save_encoded_image(response.json()['images'][0], 'dog.png')
    with open('dog.png', 'rb') as photo:
        await message.reply_photo(photo, caption=message.text)


if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True)