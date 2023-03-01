import psycopg2
import json
import base64
import requests
import random
import math
import time
import os
from googletrans import Translator
import threading

from aiogram import types, executor, Dispatcher, Bot
from aiogram.types import ReplyKeyboardMarkup, InlineKeyboardMarkup, InlineKeyboardButton, InputFile

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


def cut_prompt(model: str, prompt: str):
  if model.find('Inkpunk') != -1:
    prompt = 'nvinkpunk ' + prompt
  elif model.find('redshift') != -1:
    prompt = 'redshift style ' + prompt
  elif model.find('comic-diffusion') != -1:
    prompt = 'charliebo artstyle ' + prompt
  elif model.find('robo-diffusion') != -1:
    prompt = 'nousr robot ' + prompt
  elif model.find('openjourneyAka_v1') != -1:
    prompt = 'mdjrny-v4 style ' + prompt
  elif model.find('ghibli') != -1:
    prompt = 'ghibli style ' + prompt
  elif model.find('future') != -1:
    prompt = 'future style ' + prompt
  elif model.find('cuteRichstyle15_cuteRichstyle') != -1:
    prompt = 'cbzbb style ' + prompt
  elif model.find('synthwavepunk') != -1:
    prompt = 'NVINKPUNK ' + prompt
  elif model.find('realisticVision') != -1:
    prompt = 'ANALOG STYLE ' + prompt
  elif model.find('KhrushchevkaDiffusion') != -1:
    prompt = 'khrushchevka ' + prompt
  elif model.find('hrl31') != -1:
    prompt = 'PHOTOREALISM ' + prompt
  return prompt

def create_post(type: str, hr: str):
    print('create_post')
    txt2img_url = 'http://127.0.0.1:7861/sdapi/v1/txt2img'
    cur.execute("SELECT prompt, steps, width, height, scale, model, negative, sampler from prompts")
    rows = cur.fetchall()
    for row in rows:
        if type == 'min':
            steps = 20
            width = 256
            height = 256
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
        prompt = row[0]
        # добавляем промпту префикс модельки
        cut_prompt(row[5], prompt)
        #prompt = '```'+prompt+'```'
        count = 1
        if type == 'gen4' or type == 'min' or (type == 'gen' and hr == 'hr4'):
            count = 4

        if hr == 'hr' or hr == 'hr4':
            data = {
                'prompt': prompt,
                'steps':  steps,
                'width':  width,
                'height': height,
                'cfg_scale': cfg_scale,
                'model':row[5],
                'negative_prompt': row[6],
                'sampler_index': row[7],
                'batch_size': count,
                'enable_hr': 'true',
                'denoising_strength': 0.7,
                'firstphase_width': 0,
                'firstphase_height': 0,
                'hr_scale': 2,
                'hr_upscaler': 'R-ESRGAN 4x+',
                'hr_second_pass_steps': 0,
                'hr_resize_x': 0,
                'hr_resize_y': 0
            }
        else:
            data = {
                'prompt': prompt,
                'steps':  steps,
                'width':  width,
                'height': height,
                'cfg_scale': cfg_scale,
                'model':row[5],
                'negative_prompt': row[6],
                'sampler_index': row[7],
                'batch_size': count
            }
        # для вывода в телегу
        data2 = {
            #'prompt': prompt,
            'steps':  steps,
            'width':  width,
            'height': height,
            'cfg_scale': cfg_scale,
            'model':row[5],
            'negative_prompt': row[6],
            'sampler_index': row[7]
        }
    #con.close()
    #print(len(data))
    response = submit_post(txt2img_url, data)
    #print(response.json())
    save_encoded_image(response.json()['images'][0], 'dog.png')
    if type == 'gen4' or type == 'min' or (type == 'gen' and hr == 'hr4'):
        save_encoded_image(response.json()['images'][1], 'dog2.png')
        save_encoded_image(response.json()['images'][2], 'dog3.png')
        save_encoded_image(response.json()['images'][3], 'dog4.png')
    print('capture save')
    return data2

def submit_post(url: str, data: dict):
    return requests.post(url, data=json.dumps(data))

def submit_get(url: str, data: dict):
    return requests.get(url, data=json.dumps(data))

def save_encoded_image(b64_image: str, output_path: str):
    """
    Save the given image to the given output path.
    """
    with open(output_path, "wb") as image_file:
        image_file.write(base64.b64decode(b64_image))

def get_ikb() -> InlineKeyboardMarkup:
    ikb = InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton('min', callback_data='min'),
         InlineKeyboardButton('max', callback_data='max')],[
         InlineKeyboardButton('gen', callback_data='gen'),
         InlineKeyboardButton('gen4', callback_data='gen4'),
         InlineKeyboardButton('gen_hr', callback_data='gen_hr')],[
         #InlineKeyboardButton('gen_hr4', callback_data='gen_hr4')
         InlineKeyboardButton('random', callback_data='random'),
         InlineKeyboardButton('option', callback_data='option')],[
         InlineKeyboardButton('size', callback_data='size'),
         InlineKeyboardButton('scale', callback_data='scale'),
         InlineKeyboardButton('steps', callback_data='steps'),
         InlineKeyboardButton('samplers', callback_data='samplers'),
         InlineKeyboardButton('models', callback_data='models')]
    ])
    return ikb

# статус. Не работает
@dp.message_handler(commands=['status'])
async def cmd_status(message: types.Message) -> None:
    print('status')
    response = submit_get('http://127.0.0.1:7861/sdapi/v1/progress?skip_current_image=false', '')
    await bot.send_message(chat_id=message.from_user.id, text=response.json())

@dp.message_handler(commands=['start'])
async def cmd_start(message: types.Message) -> None:
    await message.reply('Введи текст', reply_markup=types.ReplyKeyboardRemove())

@dp.message_handler(commands=['negative'])
async def send_welcome(message: types.Message):
    button_text = message.text
    print('negative')
    cur.execute("UPDATE prompts set negative = %s where user_id = %s", (button_text.replace('/negative ', ''), message.from_user.id))
    con.commit()
    await message.reply("Негатив записан")

# проходимся одним запросом по всем моделям
@dp.message_handler(commands=['rnd'])
async def send_welcome(message: types.Message):
    # обновить папку с моделями
    requests.post('http://127.0.0.1:7861/sdapi/v1/refresh-checkpoints', '')
    # вытянуть модели
    response = submit_get('http://127.0.0.1:7861/sdapi/v1/sd-models', '')
    arr = []
    #i = 0
    # заполняем актуальный массив моделей в arr
    for item in response.json():
        arr.append(item['title'])
    # запускаем цикл по списку
    for title in arr:
        #if i < 5:
        # на всякий случай пишем модель в БД. Может надо будет потом убрать, хз
        cur.execute("UPDATE prompts set model = %s where user_id = %s", (title, message.from_user.id))
        con.commit()
        # меняем модель в памяти
        submit_post('http://127.0.0.1:7861/sdapi/v1/options', {'sd_model_checkpoint': title})
        time.sleep(5)
        data = create_post('gen', '')
        # пока не через media
        with open('dog.png', 'rb') as photo:
            await bot.send_photo(message.from_user.id,photo,title)
            #i += 1
    # Для вывода итогов в конце тянем промпт и описание из data
    cur.execute("SELECT prompt from prompts")
    rows = cur.fetchall()
    await message.reply(rows[0])
    await message.reply(data)

@dp.callback_query_handler(text='random')
async def rnd(callback: types.CallbackQuery) -> None:
    arr = []
    with open('random.json', encoding='utf-8') as json_file:
        data = json.load(json_file)
        for i in data['messages']:
            if i['text'] != '':
                arr.append(i['text'])
    n = math.ceil(random.uniform(0, len(arr) - 1))
    translator = Translator()
    translated = translator.translate(arr[n])
    prompt = translated.text
    cur.execute("UPDATE prompts set prompt = %s where user_id = %s", (prompt, callback.from_user.id))
    con.commit()

    scale = math.ceil(random.uniform(1, 20))
    cur.execute("UPDATE prompts set scale = %s where user_id = %s", (scale, callback.from_user.id))
    con.commit()

    steps = math.ceil(random.uniform(20, 60))
    #steps = 20
    cur.execute("UPDATE prompts set steps = %s where user_id = %s", (steps, callback.from_user.id))
    con.commit()

    # обновить папку с моделями
    requests.post('http://127.0.0.1:7861/sdapi/v1/refresh-checkpoints', '')
    # вытянуть модели
    response = submit_get('http://127.0.0.1:7861/sdapi/v1/sd-models', '')
    arr = []
    for item in response.json():
        arr.append(item['title'])
    model = math.ceil(random.uniform(1, len(arr))) - 1
    print(arr[model])
    cur.execute("UPDATE prompts set model = %s where user_id = %s", (arr[model], callback.from_user.id))
    con.commit()
    # меняем модель в памяти
    submit_post('http://127.0.0.1:7861/sdapi/v1/options', {'sd_model_checkpoint': arr[model]})
    time.sleep(5)

    # промпты
    n = math.ceil(random.uniform(0, len(arr)-1))
    translator = Translator()
    txt = data['messages'][n]['text']
    translated = translator.translate(txt)
    prompt = translated.text
    cut_prompt(arr[model], prompt)
    print(prompt)
    cur.execute("UPDATE prompts set prompt = %s where user_id = %s", (prompt, callback.from_user.id))
    con.commit()

    # вытянуть семплеры
    response = submit_get('http://127.0.0.1:7861/sdapi/v1/samplers', '')
    arr = []
    for item in response.json():
        arr.append(item['name'])
    sampler = math.ceil(random.uniform(1, len(arr)))-1
    cur.execute("UPDATE prompts set sampler = %s where user_id = %s", (arr[sampler], callback.from_user.id))
    con.commit()

    print("new prompt")
    data = create_post('gen4', '')
    media = types.MediaGroup()
    media.attach_photo(types.InputFile('dog.png'), json.dumps(data))
    media.attach_photo(types.InputFile('dog2.png'), json.dumps(data))
    media.attach_photo(types.InputFile('dog3.png'), json.dumps(data))
    media.attach_photo(types.InputFile('dog4.png'), json.dumps(data))
    await callback.message.delete()
    await bot.send_media_group(callback.message.chat.id, media=media)
    await bot.send_message(chat_id=callback.from_user.id, text='Выбираем заново', reply_markup=get_ikb())
    await bot.send_message(chat_id=callback.from_user.id, text=prompt)

@dp.callback_query_handler(text='min')
async def cb_menu_1(callback: types.CallbackQuery) -> None:
    data = create_post('min', '')
    media = types.MediaGroup()
    media.attach_photo(types.InputFile('dog.png'), json.dumps(data))
    media.attach_photo(types.InputFile('dog2.png'), json.dumps(data))
    media.attach_photo(types.InputFile('dog3.png'), json.dumps(data))
    media.attach_photo(types.InputFile('dog4.png'), json.dumps(data))
    await callback.message.delete()
    await bot.send_media_group(callback.message.chat.id, media=media)
    await bot.send_message(chat_id=callback.from_user.id, text='Выбираем заново', reply_markup=get_ikb())


@dp.callback_query_handler(text='max')
async def cb_menu_2(callback: types.CallbackQuery) -> None:
    data = create_post('max', '')
    print(147)
    #print(data)
    with open('dog.png', 'rb') as photo:
        await callback.message.delete()
        await callback.message.answer_photo(photo, caption=data, reply_markup=types.ReplyKeyboardRemove())
        await bot.send_message(chat_id=callback.from_user.id, text='Выбираем заново', reply_markup=get_ikb())


@dp.callback_query_handler(text='gen')
async def cb_menu_3(callback: types.CallbackQuery) -> None:
    print('gen')
    #print(callback.message.message_id)
    data = create_post('gen', '')
    with open('dog.png', 'rb') as photo:
        await callback.message.delete()
        await callback.message.answer_photo(photo, caption=data, reply_markup=types.ReplyKeyboardRemove())
        await bot.send_message(chat_id=callback.from_user.id, text='Выбираем заново', reply_markup=get_ikb())

@dp.callback_query_handler(text='gen_hr')
async def cb_menu_1(callback: types.CallbackQuery) -> None:
    print('gen_hr')
    data = create_post('gen', 'hr')
    with open('dog.png', 'rb') as photo:
        await callback.message.delete()
        await bot.send_document(callback.from_user.id, photo)
        await bot.send_message(chat_id=callback.from_user.id, text=data, reply_markup=get_ikb())

@dp.callback_query_handler(text='gen_hr4')
async def cb_menu_5(callback: types.CallbackQuery) -> None:
    print('gen_hr4')
    data = create_post('gen', 'hr4')
    #media = types.MediaGroup()
    with open('dog.png', 'rb') as photo:
        await callback.message.delete()
        await bot.send_document(callback.from_user.id, photo)
    with open('dog2.png', 'rb') as photo:
        await bot.send_document(callback.from_user.id, photo)
    with open('dog3.png', 'rb') as photo:
        await bot.send_document(callback.from_user.id, photo)
    with open('dog4.png', 'rb') as photo:
        await bot.send_document(callback.from_user.id, photo)
        await bot.send_message(chat_id=callback.from_user.id, text=data, reply_markup=get_ikb())
    """
    media.attach_photo(types.InputFile('dog.png'), json.dumps(data))
    media.attach_photo(types.InputFile('dog2.png'), json.dumps(data))
    media.attach_photo(types.InputFile('dog3.png'), json.dumps(data))
    media.attach_photo(types.InputFile('dog4.png'), json.dumps(data))
    await callback.message.delete()
    await bot.send_media_group(callback.message.chat.id, media=media)
    await bot.send_message(chat_id=callback.from_user.id, text=data, reply_markup=get_ikb())
    """

@dp.callback_query_handler(text='gen4')
async def cb_menu_6(callback: types.CallbackQuery) -> None:
    print('gen4')
    #print(callback.message.message_id)
    data = create_post('gen4', '')
    media = types.MediaGroup()
    media.attach_photo(types.InputFile('dog.png'), json.dumps(data))
    media.attach_photo(types.InputFile('dog2.png'), json.dumps(data))
    media.attach_photo(types.InputFile('dog3.png'), json.dumps(data))
    media.attach_photo(types.InputFile('dog4.png'), json.dumps(data))
    await callback.message.delete()
    await bot.send_media_group(callback.message.chat.id, media=media)
    await bot.send_message(chat_id=callback.from_user.id, text='Выбираем заново', reply_markup=get_ikb())



def get_size() -> InlineKeyboardMarkup:
    ikb = InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton('w', callback_data='w'),
         InlineKeyboardButton('h', callback_data='h'),
         InlineKeyboardButton('256*256',  callback_data='size|256_256'),
         ],[
         InlineKeyboardButton('512*512',  callback_data='size|512_512'),
         InlineKeyboardButton('512*768',  callback_data='size|512_768'),
         InlineKeyboardButton('512*1024', callback_data='size|512_1024'),
         InlineKeyboardButton('512*1280', callback_data='size|512_1280')
         ],[
         InlineKeyboardButton('768*512',  callback_data='size|768_512'),
         InlineKeyboardButton('768*768',  callback_data='size|768_768'),
         InlineKeyboardButton('768*1024', callback_data='size|768_1024'),
         InlineKeyboardButton('768*1280', callback_data='size|768_1280')
         ],[
         InlineKeyboardButton('1024*512', callback_data='size|1024_512'),
         InlineKeyboardButton('1024*768', callback_data='size|1024_768'),
         InlineKeyboardButton('1024*1024', callback_data='size|1024_1024'),
         InlineKeyboardButton('1024*1280', callback_data='size|1024_1280')
         ],[
         InlineKeyboardButton('1280*512', callback_data='size|1280_512'),
         InlineKeyboardButton('1280*768', callback_data='size|1280_768'),
         InlineKeyboardButton('1280*1024', callback_data='size|1280_1024'),
         InlineKeyboardButton('1280*1280', callback_data='size|1280_1280')
         ],[
         InlineKeyboardButton('gen', callback_data='gen'),
         InlineKeyboardButton('gen4', callback_data='gen4'),
         InlineKeyboardButton('gen_hr', callback_data='gen_hr')
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
         InlineKeyboardButton('11', callback_data='scale|11'),
         InlineKeyboardButton('12', callback_data='scale|12'),
         InlineKeyboardButton('13', callback_data='scale|13'),
         InlineKeyboardButton('15', callback_data='scale|15'),
         InlineKeyboardButton('20', callback_data='scale|20')],[
         InlineKeyboardButton('gen', callback_data='gen'),
            InlineKeyboardButton('gen4', callback_data='gen4'),
         InlineKeyboardButton('gen_hr', callback_data='gen_hr')
         ]
    ])
    return ikb

def get_steps() -> InlineKeyboardMarkup:
    ikb = InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton('20',  callback_data='steps|20'),
         InlineKeyboardButton('30',  callback_data='steps|30'),
         InlineKeyboardButton('40',  callback_data='steps|40'),
         InlineKeyboardButton('50',  callback_data='steps|50'),
         InlineKeyboardButton('60',  callback_data='steps|60'),
         InlineKeyboardButton('80',  callback_data='steps|80'),
         InlineKeyboardButton('100', callback_data='steps|100')],[
         InlineKeyboardButton('gen', callback_data='gen'),
         InlineKeyboardButton('gen4', callback_data='gen4'),
         InlineKeyboardButton('gen_hr', callback_data='gen_hr')
         ]
    ])
    return ikb

# получить список моделей и вывести его клавиатурой
def get_models() -> InlineKeyboardMarkup:
    print('get_models')
    # обновить папку с моделями
    requests.post('http://127.0.0.1:7861/sdapi/v1/refresh-checkpoints', '')
    # вытянуть модели
    response = submit_get('http://127.0.0.1:7861/sdapi/v1/sd-models', '')
    arr = []
    arr2 = []
    i = 1
    for item in response.json():
        arr.append(InlineKeyboardButton(item['model_name'], callback_data='models|'+item['model_name']))
        if i % 3 == 0:
             arr2.append(arr)
             arr = []
        i += 1
    if arr != []:
        arr2.append(arr)
    arr2.append([InlineKeyboardButton('gen', callback_data='gen'), InlineKeyboardButton('gen4', callback_data='gen4'), InlineKeyboardButton('gen_hr', callback_data='gen_hr')])
    ikb = InlineKeyboardMarkup(inline_keyboard=arr2)
    return ikb

# получить список семплеров и вывести его клавиатурой
def get_samplers() -> InlineKeyboardMarkup:
    print('get_samplers')
    # вытянуть семплеры
    response = submit_get('http://127.0.0.1:7861/sdapi/v1/samplers', '')
    arr = []
    arr2 = []
    i = 1
    for item in response.json():
        arr.append(InlineKeyboardButton(item['name'], callback_data='samplers|'+item['name']))
        if i % 3 == 0:
             arr2.append(arr)
             arr = []
        i += 1
    if arr != []:
        arr2.append(arr)
    arr2.append([InlineKeyboardButton('gen', callback_data='gen'), InlineKeyboardButton('gen4', callback_data='gen4'), InlineKeyboardButton('gen_hr', callback_data='gen_hr')])
    ikb = InlineKeyboardMarkup(inline_keyboard=arr2)
    return ikb

@dp.callback_query_handler(text='option')
async def cb_menu_7(callback: types.CallbackQuery) -> None:
    await callback.message.edit_text('size', reply_markup=get_size())


@dp.callback_query_handler(text_startswith="scale")
async def cb_menu_8(callback: types.CallbackQuery) -> None:
    print('scale')
    if callback.data != 'scale':
        s = callback.data.split("|")[1]
        cur.execute("UPDATE prompts set scale = %s where user_id = %s", (s, callback.from_user.id))
        con.commit()
        call = get_steps()
    else:
        call = get_scale()
    await callback.message.edit_text('steps', reply_markup=call)


@dp.callback_query_handler(text_startswith="steps")
async def cb_menu_9(callback: types.CallbackQuery) -> None:
    print('steps')
    if callback.data != 'steps':
        s = callback.data.split("|")[1]
        cur.execute("UPDATE prompts set steps = %s where user_id = %s", (s, callback.from_user.id))
        con.commit()
        call = get_samplers()
    else:
        call = get_steps()
    await callback.message.edit_text('samplers', reply_markup=call)


@dp.callback_query_handler(text_startswith="samplers")
async def cb_menu_10(callback: types.CallbackQuery) -> None:
    print('samplers')
    if callback.data != 'samplers':
        s = callback.data.split("|")[1]
        cur.execute("UPDATE prompts set sampler = %s where user_id = %s", (s, callback.from_user.id))
        con.commit()
        call = get_models()
    else:
        call = get_samplers()
    await callback.message.edit_text('models', reply_markup=call)


# тыкнули на модельку
@dp.callback_query_handler(text_startswith="models")
async def cb_menu_11(callback: types.CallbackQuery) -> None:
    print('models')
    if callback.data != 'models':
        s = callback.data.split("|")[1]
        response = submit_get('http://127.0.0.1:7861/sdapi/v1/sd-models', '')
        result = [x['title'] for x in response.json() if x["model_name"]==s]
        # меняем модель в памяти
        submit_post('http://127.0.0.1:7861/sdapi/v1/options', {'sd_model_checkpoint':result[0]})
        cur.execute("UPDATE prompts set model = %s where user_id = %s", (result[0], callback.from_user.id))
        con.commit()
        await callback.message.delete()
        await bot.send_message(chat_id=callback.from_user.id,
                               text='Тык',
                               reply_markup=get_ikb())
    else:
        await callback.message.edit_text('models', reply_markup=get_models())


@dp.callback_query_handler(text_startswith="size")
async def cb_menu_12(callback: types.CallbackQuery) -> None:
    print('size')
    if callback.data != 'size':
        w = callback.data.split("|")[1].split('_')[0]
        h = callback.data.split("|")[1].split('_')[1]
        cur.execute("UPDATE prompts set width = %s, height = %s where user_id = %s", (w, h, callback.from_user.id))
        con.commit()
        call = get_scale()
    else:
        call = get_size()
    await callback.message.edit_text('scale', reply_markup=call)


@dp.message_handler()
async def all_msg_handler(message: types.Message):
    print('msg')
    button_text = message.text
    translator = Translator()
    translated = translator.translate(button_text)
    prompt = translated.text
    cur.execute("UPDATE prompts set prompt = %s where user_id = %s", (prompt, message.from_user.id))
    con.commit()
    print("Record inserted successfully")
    await bot.send_message(chat_id=message.from_user.id,
                           text='Выбираем',
                           reply_markup=get_ikb())

if __name__ == '__main__':
    executor.start_polling(dp,
                           skip_updates=True)