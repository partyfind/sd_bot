# 900510503:AAG5Xug_JEERhKlf7dpOpzxXcJIzlTbWX1M
# https://docs.aiogram.dev/en/latest/
from aiogram import Bot, Dispatcher, types
from aiogram.utils import executor
from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup
from aiogram.types import InputMediaPhoto
import subprocess
import time
import requests
import io
import base64
import webuiapi, datetime


# -------- GLOBAL ----------

API_TOKEN = '900510503:AAG5Xug_JEERhKlf7dpOpzxXcJIzlTbWX1M'
bot = Bot(token=API_TOKEN)
dp = Dispatcher(bot)
host = '127.0.0.1'
port = '7861'
api = webuiapi.WebUIApi(host=host, port=port)
local = 'http://'+host+':'+port
process = None
sd = '❌'

# -------- FUNCTIONS ----------

# Запуск SD через subprocess и запись в глобальную переменную process
def start_sd():
    global process
    if not process:
        print('start_process sd')
        try:
            process = subprocess.Popen(['python', 'launch.py', '--nowebui', '--xformers'])
            # TODO stderr, stdout выводить в сообщение телеграм
        except subprocess.CalledProcessError as e:
            print("e:", e)

# Остановка SD
def stop_sd():
    global process, sd
    if process:
        print('stop_process sd')
        process.terminate()
        process = None
        sd = '❌'

# Проверка связи до запущенной локальной SD с nowebui
def ping(status: str):
    n = 0
    url = local+'/docs'
    if status == 'stop':
        while n == 200:
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
        return True
    else:
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
        return True

# -------- MENU ----------
# Стартовое меню
def getStart() -> InlineKeyboardMarkup:
    st = InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton('sd'+sd, callback_data='sd'),
         InlineKeyboardButton('opt',   callback_data='opt'),
         InlineKeyboardButton('gen',   callback_data='gen'),
         InlineKeyboardButton('help',  callback_data='help')]
    ])
    return st

# Меню опций
def getOpt() -> InlineKeyboardMarkup:
    opt = InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton('scripts',  callback_data='scripts'),
         InlineKeyboardButton('settings', callback_data='settings'),
         InlineKeyboardButton('prompt',   callback_data='prompt')]
    ])
    return opt

# Меню генераций
def getGen() -> InlineKeyboardMarkup:
    gen = InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton('gen1', callback_data='gen1'),
         InlineKeyboardButton('gen4', callback_data='gen4'),
         InlineKeyboardButton('gen10', callback_data='gen10'),
         InlineKeyboardButton('gen_hr', callback_data='gen_hr'),
         InlineKeyboardButton('gen_hr4', callback_data='gen_hr4')]
    ])
    return gen

def pilToImages(pilImages):
    media_group = []
    for image in pilImages:
        image_buffer = io.BytesIO()
        image.save(image_buffer, format='PNG')
        image_buffer.seek(0)
        media_group.append(types.InputMediaPhoto(media=image_buffer, reply_markup=InlineKeyboardMarkup().add(
            InlineKeyboardButton("Button 1", callback_data="btn1")
        )))
    return media_group

# -------- COMMANDS ----------
# start/help
@dp.message_handler(commands=['help'])
@dp.message_handler(commands=['start'])
async def cmd_start(message: types.Message) -> None:
    print('cmd_start')
    await message.reply('Это бот для локального завуска SD.\n/opt\n/gen\n/help', reply_markup=getStart())

# Получить опции
@dp.message_handler(commands=['opt'])
async def cmd_opt(message: types.Message) -> None:
    print('cmd_opt')
    await message.reply('Опции', reply_markup=getOpt())

# Получить опции inline
@dp.callback_query_handler(text='opt')
async def inl_opt(callback: types.CallbackQuery) -> None:
    print('inl_opt')
    await callback.message.edit_text('Опции', reply_markup=getOpt())

# Получить опции inline
@dp.callback_query_handler(text='help')
async def inl_help(callback: types.CallbackQuery) -> None:
    print('inl_help')
    await callback.message.edit_text('Опции', reply_markup=getOpt())

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
        start_sd()
        sd = '⌛'
        await callback.message.edit_text('Запускаем SD', reply_markup=getStart())
        ping('start')
        sd = '✅'
        await callback.message.edit_text('SD запущена \n/opt\n/gen\n/help', reply_markup=getStart())

# Остановка SD по /stop
@dp.message_handler(commands=['stop'])
async def cmd_stop(message: types.Message) -> None:
    print('cmd_stop')
    global sd
    stop_sd()
    sd = '⌛' # ?
    ping('stop')
    sd = '❌'
    await bot.send_message(chat_id=message.from_user.id, text='SD остановлена', reply_markup=getOpt())

# Вызов меню генераций
@dp.callback_query_handler(text='gen')
async def inl_gen(callback: types.CallbackQuery) -> None:
    print('inl_gen')
    await callback.message.edit_text('Виды генераций', reply_markup=getGen())

# Генерация одной картинки
@dp.callback_query_handler(text='gen1')
async def inl_gen1(callback: types.CallbackQuery) -> None:
    print('inl_gen1')
    payload = {
        "prompt": "cat in car",
        "steps": 5
    }
    response = requests.post(url=local+'/sdapi/v1/txt2img', json=payload)
    photo = base64.b64decode(response.json()['images'][0])
    await callback.message.delete()
    await callback.message.answer_photo(photo, caption='Готово', reply_markup=getGen())

# Генерация нескольких картинок
@dp.callback_query_handler(text='gen4')
async def inl_gen4(callback: types.CallbackQuery) -> None:
    print('inl_gen4')
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
    media1 = InputMediaPhoto(
        "https://picsum.photos/200/300",  # Замените ссылками на реальные изображения
        caption="Caption for first photo",
        reply_markup=InlineKeyboardMarkup().add(
            InlineKeyboardButton("Button 1", callback_data="btn1")
        )
    )
    await bot.send_media_group(chat_id=callback.from_user.id, media=pilToImages(result1.images))
    #await callback.message.delete()
    #await callback.message.edit_media(media=pilToImages(result1.images), reply_markup=getGen())
    #await callback.message.answer_media_group(media=pilToImages(result1.images), reply_markup=getStart())

# -------- BOT POLLING ----------
if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True)

# -------- COPYRIGHT ----------
# Мишген
# join https://t.me/mishgenai