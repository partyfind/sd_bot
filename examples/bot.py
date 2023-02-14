import psycopg2
import json
import base64
import requests
from aiogram import types, executor, Dispatcher, Bot
from aiogram.types import ReplyKeyboardMarkup, InlineKeyboardMarkup, InlineKeyboardButton
#from aiogram.dispatcher.filters import Text
#from aiogram.utils.callback_data import CallbackData

#from config import TOKEN_API

con = psycopg2.connect(
  database="postgres",
  user="postgres",
  password="postgres",
  host="localhost",
  port="5432"
)

print("Database opened successfully")
cur = con.cursor()

bot = Bot('5815882861:AAHVGTfEfozTaU0yRHJEEaYv7gSi4Ag_WBw')
dp = Dispatcher(bot)

def create_post(type: str):
    txt2img_url = 'http://127.0.0.1:7861/sdapi/v1/txt2img'
    cur.execute("SELECT prompt, steps, width, height, scale, model, negative from prompts")
    rows = cur.fetchall()
    for row in rows:
        if type == 'min':
            steps = 20
            width = 512
            height = 512
            cfg_scale = 7
        elif type == 'max':
            steps = 100
            width = 1024
            height = 1024
            cfg_scale = 15
        else:
            steps = row[1]
            width = row[2]
            height = row[3]
            cfg_scale = row[4]
        data = {
            'prompt': row[0],
            'steps':  steps,
            'width':  width,
            'height': height,
            'cfg_scale': cfg_scale,
            'sd_model_checkpoint':row[5],
            'negative_prompt': row[6]
        }
        prompt = row[0]
    #con.close()
    response = submit_post(txt2img_url, data)
    save_encoded_image(response.json()['images'][0], 'dog.png')
    print('dog save')
    return data

def submit_post(url: str, data: dict):
    return requests.post(url, data=json.dumps(data))


def save_encoded_image(b64_image: str, output_path: str):
    """
    Save the given image to the given output path.
    """
    with open(output_path, "wb") as image_file:
        image_file.write(base64.b64decode(b64_image))

def get_ikb() -> InlineKeyboardMarkup:
    ikb = InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton('min', callback_data='min'),
         InlineKeyboardButton('max', callback_data='max'),
         InlineKeyboardButton('last', callback_data='last'),
         InlineKeyboardButton('option', callback_data='option'), ]
    ])
    return ikb


@dp.message_handler(commands=['start'])
async def cmd_start(message: types.Message) -> None:
    await message.reply('Введи текст', reply_markup=types.ReplyKeyboardRemove())


@dp.callback_query_handler(text='min')
async def cb_menu_1(callback: types.CallbackQuery) -> None:
    data = create_post('min')
    with open('dog.png', 'rb') as photo:
        await callback.message.reply_photo(photo, caption=data, reply_markup=types.ReplyKeyboardRemove())


@dp.callback_query_handler(text='max')
async def cb_menu_1(callback: types.CallbackQuery) -> None:
    data = create_post('max')
    with open('dog.png', 'rb') as photo:
        await callback.message.reply_photo(photo, caption=data, reply_markup=types.ReplyKeyboardRemove())


@dp.callback_query_handler(text='last')
async def cb_menu_1(callback: types.CallbackQuery) -> None:
    data = create_post('last')
    with open('dog.png', 'rb') as photo:
        await callback.message.reply_photo(photo, caption=data, reply_markup=types.ReplyKeyboardRemove())


def get_size() -> InlineKeyboardMarkup:
    ikb = InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton('w', callback_data='w'),
         InlineKeyboardButton('h', callback_data='h'),
         InlineKeyboardButton('256*256',  callback_data='size|256_256'),
         ],[
         InlineKeyboardButton('512*512',  callback_data='size|512_512'),
         InlineKeyboardButton('512*768',  callback_data='size|512_768'),
         InlineKeyboardButton('512*1024', callback_data='size|512_1024')
         ],[
         InlineKeyboardButton('768*512',  callback_data='size|768_512'),
         InlineKeyboardButton('768*768',  callback_data='size|768_768'),
         InlineKeyboardButton('768*1024', callback_data='size|768_1024')
         ],[
         InlineKeyboardButton('1024*512', callback_data='size|1024_512'),
         InlineKeyboardButton('1024*768', callback_data='size|1024_768'),
         InlineKeyboardButton('1024*1024', callback_data='size|1024_1024')
         ]
    ])
    return ikb

def get_scale() -> InlineKeyboardMarkup:
    ikb = InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton('5', callback_data='scale|5'),
         InlineKeyboardButton('6', callback_data='scale|6'),
         InlineKeyboardButton('7',  callback_data='scale|7'),
         InlineKeyboardButton('8',  callback_data='scale|8'),
         InlineKeyboardButton('9',  callback_data='scale|9'),
         InlineKeyboardButton('10', callback_data='scale|10')],[
         InlineKeyboardButton('15', callback_data='scale|15'),
         InlineKeyboardButton('20', callback_data='scale|20')
         ]
    ])
    return ikb

def get_steps() -> InlineKeyboardMarkup:
    ikb = InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton('20',  callback_data='steps|20'),
         InlineKeyboardButton('30',  callback_data='steps|30'),
         InlineKeyboardButton('40',  callback_data='steps|40'),
         InlineKeyboardButton('50',  callback_data='steps|50')],[
         InlineKeyboardButton('60',  callback_data='steps|60'),
         InlineKeyboardButton('80',  callback_data='steps|80'),
         InlineKeyboardButton('100', callback_data='steps|100')
         ]
    ])
    return ikb

@dp.callback_query_handler(text='option')
async def cb_menu_1(callback: types.CallbackQuery) -> None:
    await callback.message.edit_text('size',
                                     reply_markup=get_size())


@dp.callback_query_handler(text_startswith="scale")
async def cb_menu_1(callback: types.CallbackQuery) -> None:
    s = callback.data.split("|")[1]
    cur.execute("UPDATE prompts set scale = %s where user_id = %s", (s, callback.from_user.id))
    con.commit()
    await callback.message.edit_text('steps',
                                     reply_markup=get_steps())


@dp.callback_query_handler(text_startswith="steps")
async def cb_menu_1(callback: types.CallbackQuery) -> None:
    s = callback.data.split("|")[1]
    cur.execute("UPDATE prompts set steps = %s where user_id = %s", (s, callback.from_user.id))
    con.commit()
    data = create_post('last')
    with open('dog.png', 'rb') as photo:
        await callback.message.reply_photo(photo, caption=data, reply_markup=types.ReplyKeyboardRemove())


@dp.callback_query_handler(text_startswith="size")
async def cb_menu_1(callback: types.CallbackQuery) -> None:
    w = callback.data.split("|")[1].split('_')[0]
    h = callback.data.split("|")[1].split('_')[1]
    cur.execute("UPDATE prompts set width = %s, height = %s where user_id = %s", (w, h, callback.from_user.id))
    con.commit()
    await callback.message.edit_text('scale',
                                     reply_markup=get_scale())


@dp.callback_query_handler(text='menu_back')
async def cb_menu_back(callback: types.CallbackQuery) -> None:
    await callback.message.edit_text(text='Какой-то текст - описание',
                                     reply_markup=get_ikb())

@dp.message_handler()
async def all_msg_handler(message: types.Message):
    button_text = message.text
    cur.execute("UPDATE prompts set prompt = %s where user_id = %s", (button_text, message.from_user.id))
    con.commit()
    print("Record inserted successfully")
    await bot.send_message(chat_id=message.from_user.id,
                           text='Выбираем',
                           reply_markup=get_ikb())

if __name__ == '__main__':
    executor.start_polling(dp,
                           skip_updates=True)