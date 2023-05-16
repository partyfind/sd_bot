# https://github.com/mix1009/sdwebuiapi
import webuiapi
import base64
from aiogram import Bot, Dispatcher, types
from aiogram.utils import executor
from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup, Message, CallbackQuery, InputMediaPhoto
import asyncio
import io
import json
from aiogram import Bot, Dispatcher, types
from PIL import Image

API_TOKEN = '900510503:AAG5Xug_JEERhKlf7dpOpzxXcJIzlTbWX1M'

bot = Bot(token=API_TOKEN)
dp = Dispatcher(bot)

# create API client
#api = webuiapi.WebUIApi()

# create API client with custom host, port
api = webuiapi.WebUIApi(host='127.0.0.1', port=7861)

# create API client with custom host, port and https
#api = webuiapi.WebUIApi(host='webui.example.com', port=443, use_https=True)

# create API client with default sampler, steps.
#api = webuiapi.WebUIApi(sampler='Euler a', steps=20)

# optionally set username, password when --api-auth is set on webui.
#api.set_auth('username', 'password')


# images contains the returned images (PIL images)
#result1.images

# image is shorthand for images[0]
#result1.image

# info contains text info about the api call
#result1.info

# info contains paramteres of the api call
#result1.parameters

#result1.image

def createimg(pilImage):
    with io.BytesIO() as bio:
        pilImage.save(bio, 'PNG')
        bio.seek(0)
    return bio

def wrap_media(bytesio, **kwargs):
    """Wraps plain BytesIO objects into InputMediaPhoto"""
    # First, rewind internal file pointer to the beginning so the contents
    #  can be read by InputFile class
    bytesio.seek(0)
    return types.InputMediaPhoto(types.InputFile(bytesio), **kwargs)

def pilToImage(pilImage):
    with io.BytesIO() as bio:
        # сохраняем изображение в байтовый поток
        pilImage.save(bio, 'PNG')
        # извлекаем байты
        bio.seek(0)
        data = bio.getvalue()
    #return types.InputMediaPhoto(data)
    return data

@dp.message_handler(commands=['start'])
async def cmd_start(message: types.Message) -> None:
    print('cmd_start')
    result1 = api.txt2img(prompt="cute cat",
                          negative_prompt="ugly, out of frame",
                          seed=1003,
                          styles=["anime"],
                          cfg_scale=8,
                          #sampler_index='DDIM',
                          steps=15,
                          #enable_hr=True,
                          #hr_scale=2,
                          #hr_upscaler=webuiapi.HiResUpscaler.Latent,
                          #hr_second_pass_steps=20,
                          #hr_resize_x=1536,
                          #hr_resize_y=1024,
                          #denoising_strength=0.4,
                          batch_size=1
                          )
    print(result1.image)
    print(result1.images)
    #photo1 = InputMediaPhoto(pilToImage(result1.images[0]), caption='Фото 1')
    #photo2 = InputMediaPhoto(pilToImage(result1.images[1]), caption='Фото 2')
    #media = types.MediaGroup()
    #for im in result1.images:
        #media.attach_photo(im, json.dumps('111'))
        #await bot.send_photo(message.chat.id, pilToImage(im))
    # создаем bytes-объект в памяти и записываем в него содержимое PngImageFile

    await bot.send_photo(message.chat.id, pilToImage(result1.image))
    #await bot.send_media_group(message.chat.id, media=media)
    #await bot.send_media_group(message.chat.id, media = [wrap_media(createimg(result1.images[0])), wrap_media(createimg(result1.images[1]))])

if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True)