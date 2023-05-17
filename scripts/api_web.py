# https://github.com/mix1009/sdwebuiapi
import webuiapi, io, datetime
from aiogram.utils import executor
from aiogram import Bot, Dispatcher, types

API_TOKEN = '900510503:AAG5Xug_JEERhKlf7dpOpzxXcJIzlTbWX1M'

bot = Bot(token=API_TOKEN)
dp = Dispatcher(bot)



# create API client with custom host, port
api = webuiapi.WebUIApi(host='127.0.0.1', port=7861)

def pilToImages(pilImages):
    media_group = []
    for image in pilImages:
        image_buffer = io.BytesIO()
        image.save(image_buffer, format='PNG')
        image_buffer.seek(0)
        media_group.append(types.InputMediaPhoto(media=image_buffer))
    return media_group

@dp.message_handler(commands=['start'])
async def cmd_start(message: types.Message) -> None:
    print('cmd_start')
    result1 = api.txt2img(prompt="cute cat",
                          negative_prompt="ugly, out of frame",
                          seed=datetime.datetime.now().strftime("%Y%m%d%H%M%S%f")[:-3],
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
                          batch_size=2
                          )
    await bot.send_media_group(chat_id=message.chat.id, media=pilToImages(result1.images))

if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True)

#------
# create API client
#api = webuiapi.WebUIApi()

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