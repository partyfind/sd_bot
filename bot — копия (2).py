"""
This bot is created for the demonstration of a usage of regular keyboards.
"""

import json
import base64
import requests
import logging

from aiogram import Bot, Dispatcher, executor, types


API_TOKEN = '5815882861:AAHVGTfEfozTaU0yRHJEEaYv7gSi4Ag_WBw'

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)

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

@dp.message_handler(commands='start')
async def start_cmd_handler(message: types.Message):
    keyboard_markup = types.ReplyKeyboardMarkup(row_width=3)
    # default row_width is 3, so here we can omit it actually
    # kept for clearness

    btns_text = ('5', '100')
    keyboard_markup.row(*(types.KeyboardButton(text) for text in btns_text))
    # adds buttons as a new row to the existing keyboard
    # the behaviour doesn't depend on row_width attribute

    more_btns_text = (
        "10",
        "20",
        "30",
        "50",
    )
    keyboard_markup.add(*(types.KeyboardButton(message.text+'|'+text) for text in more_btns_text))
    # adds buttons. New rows are formed according to row_width parameter

    await message.reply("steps", reply_markup=keyboard_markup)


@dp.message_handler()
async def all_msg_handler(message: types.Message):

    keyboard_markup = types.ReplyKeyboardMarkup(row_width=3)
    button_text = message.text
    logger.debug('The answer is %r', button_text)  # print the text we've got

    if len(button_text.split('|')) == 1:
        more_btns_text = (
            "10",
            "20",
            "30",
            "50",
        )
        keyboard_markup.add(*(types.KeyboardButton(message.text+'|'+text) for text in more_btns_text))
        await message.reply("steps", reply_markup=keyboard_markup)
    elif len(button_text.split('|')) == 2:
        more_btns_text = (
            "512*512",
            "512*768",
            "768*768",
            "1024*1024",
        )
        keyboard_markup.add(*(types.KeyboardButton(message.text+'|'+text) for text in more_btns_text))
        await message.reply("size", reply_markup=keyboard_markup)
    elif len(button_text.split('|')) == 3:
        more_btns_text = (
            "7",
            "9",
            "12",
            "15",
        )
        keyboard_markup.add(*(types.KeyboardButton(message.text+'|'+text) for text in more_btns_text))
        await message.reply("scale", reply_markup=keyboard_markup)
    else:
        txt2img_url = 'http://127.0.0.1:7861/sdapi/v1/txt2img'
        data = {
        'prompt': button_text.split('|')[0], 
        'steps': button_text.split('|')[1],
        'width': button_text.split('|')[2].split('*')[0],
        'height': button_text.split('|')[2].split('*')[1],
        'cfg_scale': button_text.split('|')[3],
        'sd_model_checkpoint':'deliberate_v11.ckpt [10a699c0f3]'
        }
        response = submit_post(txt2img_url, data)
        save_encoded_image(response.json()['images'][0], 'dog.png')
        with open('dog.png', 'rb') as photo:
            await message.reply_photo(photo, caption=message.text, reply_markup=types.ReplyKeyboardRemove())

if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True)