import psycopg2
import json
import base64
import requests
import time
import subprocess
from transformers import GPT2Tokenizer, GPT2LMHeadModel
tokenizer = GPT2Tokenizer.from_pretrained('distilgpt2')
tokenizer.add_special_tokens({'pad_token': '[PAD]'})
model = GPT2LMHeadModel.from_pretrained('FredZhang7/distilgpt2-stable-diffusion-v2')
from aiogram import types, executor, Dispatcher, Bot
from aiogram.types import ReplyKeyboardMarkup, InlineKeyboardMarkup, InlineKeyboardButton, InputFile
import random
import logging
from langdetect import detect

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

# Set up logging
logging.basicConfig(level=logging.INFO)

# Error handling
async def on_error(update, exception):
    logging.error(f'Update {update} caused {exception}')

# Register error handling
dp.register_errors_handler(on_error)

process = None
sd = '❌'

def start_sd():
    global process
    if not process:
        print('start_process start_sd')
        process = subprocess.Popen(['python', 'launch.py', '--nowebui', '--xformers'])

def stop_sd():
    global process
    if process:
        print('stop_process stop_sd')
        process.terminate()
        process = None

def get_random_prompt():
    arr = []
    with open('random.json', encoding='utf-8') as json_file:
        data = json.load(json_file)
        for i in data['messages']:
            if i['text'] != '':
                arr.append(i['text'])
    n = random.randint(0, len(arr) - 1)
    return arr[n]

@dp.callback_query_handler(text='strt')
async def strt(callback: types.CallbackQuery) -> None:
    global sd
    start_sd()
    print('start sd')
    await callback.message.edit_text('SD запущена', reply_markup=get_ikb())
    url = 'http://127.0.0.1:7861/docs'
    n = 0
    while n != 200:
        time.sleep(2)
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
    sd = '✅'
    await callback.message.edit_text('SD запущена', reply_markup=get_ikb())

@dp.callback_query_handler(text='stp')
async def stp(callback: types.CallbackQuery) -> None:
    global sd
    stop_sd()
    print('stop sd')
    sd = '❌'
    await callback.message.edit_text('SD остановлена', reply_markup=get_ikb())

def cut_prompt(model: str, prompt: str):
  if model.find('synthwavepunk_v2') != -1:
    prompt = 'snthwve style ' + prompt
  elif model.find('Realistic_Vision_V2.0') != -1:
    prompt = 'analog style ' + prompt
  elif model.find('protogenX34Photorealism_1') != -1:
    prompt = 'analog style ' + prompt
  elif model.find('protogenX58RebuiltScifi_10') != -1:
    prompt = 'modelshoot style ' + prompt
  elif model.find('cuteRichstyle15_cuteRichstyle') != -1:
    prompt = 'cbzbb style ' + prompt
  elif model.find('kenshi') != -1:
    prompt = 'semi-realistic ' + prompt
  elif model.find('fkingScifiV2_v21f') != -1:
    prompt = 'fking_scifi_v2 ' + prompt
  elif model.find('hrl32_hrl32') != -1:
    prompt = 'PHOTOREALISM ' + prompt
  return prompt

def create_post(type: str, hr: str):
    print('create_post')
    txt2img_url = 'http://127.0.0.1:7861/sdapi/v1/txt2img'
    cur.execute("SELECT prompt, steps, width, height, scale, model, negative, sampler from prompts")
    rows = cur.fetchall()
    for row in rows:
        steps = row[1]
        width = row[2]
        height = row[3]
        cfg_scale = row[4]
        prompt = row[0]
        # добавляем промпту префикс модельки
        prompt = cut_prompt(row[5], prompt)
        print(prompt)
        #prompt = '```'+prompt+'```'
        count = 1
        if type == 'gen4' or (type == 'gen' and hr == 'hr4'):
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
                'denoising_strength': 0.5,
                'firstphase_width': 0,
                'firstphase_height': 0,
                'hr_scale': 2,
                'hr_upscaler': 'R-ESRGAN 4x+',
                'hr_second_pass_steps': 15,
                'hr_resize_x': width*2,
                'hr_resize_y': height*2
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
    if type == 'gen4' or (type == 'gen' and hr == 'hr4'):
        save_encoded_image(response.json()['images'][1], 'dog2.png')
        save_encoded_image(response.json()['images'][2], 'dog3.png')
        save_encoded_image(response.json()['images'][3], 'dog4.png')
    print('capture save')
    return data2

def submit_post(url: str, data: dict):
    return requests.post(url, data=json.dumps(data))

def submit_get(url: str, data: dict):
    return requests.get(url, data=json.dumps(data))

def get_opt():
    cur.execute("SELECT prompt, steps, width, height, scale, negative, sampler, model from prompts")
    rows = cur.fetchall()
    for row in rows:
        prompt = row[0]
        steps = row[1]
        width = row[2]
        height = row[3]
        scale = row[4]
        negative = row[5].replace('/negative ', '')
        sampler = row[6]
        model = row[7]
        opt = f'prompt = `{prompt}` \n steps = *{steps}* \n width = *{width}* \n height = *{height}* ' \
              f'\n scale = *{scale}* \n negative = *{negative}* \n sampler = *{sampler}* \n model = *{model}*'
    return opt

def save_encoded_image(b64_image: str, output_path: str):
    """
    Save the given image to the given output path.
    """
    with open(output_path, "wb") as image_file:
        image_file.write(base64.b64decode(b64_image))

def get_ikb() -> InlineKeyboardMarkup:
    ikb = InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton('start SD'+sd, callback_data='strt'),
         InlineKeyboardButton('stop SD', callback_data='stp')],[
         InlineKeyboardButton('gen', callback_data='gen'),
         InlineKeyboardButton('gen4', callback_data='gen4'),
         InlineKeyboardButton('gen_hr', callback_data='gen_hr'),
         InlineKeyboardButton('gen_hr4', callback_data='gen_hr4')],[
         InlineKeyboardButton('get_opt', callback_data='get_opt_f'),
         InlineKeyboardButton('rndm', callback_data='random'),
         InlineKeyboardButton('rnd', callback_data='rnd'),
         InlineKeyboardButton('rnd_hr', callback_data='rnd_hr'),
         InlineKeyboardButton('rnd_rev', callback_data='rnd_rev'),
         InlineKeyboardButton('rnd_smp', callback_data='rnd_smp')],[
         InlineKeyboardButton('prmpt', callback_data='prompt'),
         InlineKeyboardButton('optn', callback_data='option')],[
         InlineKeyboardButton('size', callback_data='size'),
         InlineKeyboardButton('scale', callback_data='scale'),
         InlineKeyboardButton('steps', callback_data='steps'),
         InlineKeyboardButton('smplrs', callback_data='samplers'),
         InlineKeyboardButton('mdls', callback_data='models')]
    ])
    return ikb

# статус. Не работает
@dp.message_handler(commands=['status'])
async def cmd_status(message: types.Message) -> None:
    print('status')
    response = submit_get('http://127.0.0.1:7861/sdapi/v1/progress?skip_current_image=false', '')
    await bot.send_message(chat_id=message.from_user.id, text=response.json())

# главное меню /opt
@dp.message_handler(commands=['opt'])
async def opt(message: types.Message) -> None:
    await bot.send_message(chat_id=message.from_user.id, text='Опции', reply_markup=get_ikb())

# /stop
@dp.message_handler(commands=['stop'])
async def stop(message: types.Message) -> None:
    global sd
    stop_sd()
    sd = '❌'
    await message.reply('SD остановлена', reply_markup=get_ikb())

# /create_post_vk
@dp.message_handler(commands=['create_post_vk'])
async def stop(message: types.Message) -> None:
    result = subprocess.run(
        ['C:\OSPanel\modules\php\PHP_7.3\php.exe', "C:/OSPanel/domains/localhost/vk/create_post.php"], stdout=subprocess.PIPE, stderr=subprocess.PIPE
    )
    output = result.stdout.decode('utf-8')
    await message.reply(output, reply_markup=types.ReplyKeyboardRemove())

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

@dp.message_handler(commands=['models'])
async def getModels(message: types.Message):
    response = submit_get('http://127.0.0.1:7861/sdapi/v1/sd-models', '')
    arr = ''
    for item in response.json():
        arr = arr+'model_name '+item['model_name']+'\n'
        arr = arr+'title '+item['title']+'\n\n'
    await message.reply(arr, parse_mode=types.ParseMode.HTML)

# цикл по семплерам
@dp.callback_query_handler(text='rnd_smp')
async def rnd_smp(callback: types.CallbackQuery) -> None:
    print('rnd_smp')
    # вытянуть семплеры
    response = submit_get('http://127.0.0.1:7861/sdapi/v1/samplers', '')
    for item in response.json():
        s = item['name']
        cur.execute("UPDATE prompts set sampler = %s where user_id = %s", (s, callback.from_user.id))
        con.commit()
        data = create_post('gen', '')
        title = s + '\n/stop \n/opt '
        with open('dog.png', 'rb') as photo:
            await callback.message.answer_photo(photo, caption=title, reply_markup=types.ReplyKeyboardRemove())
    # Для вывода итогов в конце тянем промпт и описание из data
    cur.execute("SELECT prompt from prompts")
    rows = cur.fetchall()
    # callback.reply не сработает, так как на клаву нельзя ответить. Можно попробовать вытягивать последнее сообщение с промптом
    await bot.send_message(chat_id=callback.from_user.id, text=f'prompt = `{rows[0]}`', parse_mode='Markdown')
    await bot.send_message(chat_id=callback.from_user.id, text=f'data = `{data}`', parse_mode='Markdown')
    await bot.send_message(chat_id=callback.from_user.id, text='Менюшка', parse_mode='Markdown', reply_markup=get_ikb())


@dp.callback_query_handler(text='rnd_rev')
async def rnd_rev(callback: types.CallbackQuery) -> None:
    # повторение rnd
    # обновить папку с моделями
    requests.post('http://127.0.0.1:7861/sdapi/v1/refresh-checkpoints', '')
    # вытянуть модели
    response = submit_get('http://127.0.0.1:7861/sdapi/v1/sd-models', '')
    arr = []
    #i = 0
    # заполняем актуальный массив моделей в arr
    for item in response.json():
        arr.append(item['title'])
    arr = list(reversed(arr))
    await callback.message.edit_text('Ну погнали', reply_markup=get_ikb())
    await bot.send_message(chat_id=callback.from_user.id, text=get_opt(), parse_mode='Markdown')
    # запускаем цикл по списку
    for title in arr:
        #if i < 5:
        # на всякий случай пишем модель в БД. Может надо будет потом убрать, хз
        cur.execute("UPDATE prompts set model = %s where user_id = %s", (title, callback.from_user.id))
        con.commit()
        # меняем модель в памяти
        submit_post('http://127.0.0.1:7861/sdapi/v1/options', {'sd_model_checkpoint': title})
        time.sleep(5)
        data = create_post('gen', '')
        title = title + '\n/stop \n/opt '
        # пока не через media
        with open('dog.png', 'rb') as photo:
            await callback.message.answer_photo(photo, caption=title, reply_markup=types.ReplyKeyboardRemove())
            #i += 1
    # Для вывода итогов в конце тянем промпт и описание из data
    cur.execute("SELECT prompt from prompts")
    rows = cur.fetchall()
    # callback.reply не сработает, так как на клаву нельзя ответить. Можно попробовать вытягивать последнее сообщение с промптом
    await bot.send_message(chat_id=callback.from_user.id, text=f'prompt = `{rows[0]}`', parse_mode='Markdown')
    await bot.send_message(chat_id=callback.from_user.id, text=f'data = `{data}`', parse_mode='Markdown')
    await bot.send_message(chat_id=callback.from_user.id, text='Менюшка', parse_mode='Markdown', reply_markup=get_ikb())


# проходимся одним запросом по всем моделям
@dp.callback_query_handler(text='rnd')
async def rnd(callback: types.CallbackQuery) -> None:
    # обновить папку с моделями
    requests.post('http://127.0.0.1:7861/sdapi/v1/refresh-checkpoints', '')
    # вытянуть модели
    response = submit_get('http://127.0.0.1:7861/sdapi/v1/sd-models', '')
    arr = []
    #i = 0
    # заполняем актуальный массив моделей в arr
    for item in response.json():
        arr.append(item['title'])
    await callback.message.edit_text('Ну погнали', reply_markup=get_ikb())
    await bot.send_message(chat_id=callback.from_user.id, text=get_opt(), parse_mode='Markdown')
    # запускаем цикл по списку
    for title in arr:
        #if i < 5:
        # на всякий случай пишем модель в БД. Может надо будет потом убрать, хз
        cur.execute("UPDATE prompts set model = %s where user_id = %s", (title, callback.from_user.id))
        con.commit()
        # меняем модель в памяти
        submit_post('http://127.0.0.1:7861/sdapi/v1/options', {'sd_model_checkpoint': title})
        time.sleep(5)
        data = create_post('gen', '')
        title = title + '\n/stop \n/opt '
        # пока не через media
        with open('dog.png', 'rb') as photo:
            await callback.message.answer_photo(photo, caption=title, reply_markup=types.ReplyKeyboardRemove())
            #i += 1
    # Для вывода итогов в конце тянем промпт и описание из data
    cur.execute("SELECT prompt from prompts")
    rows = cur.fetchall()
    # callback.reply не сработает, так как на клаву нельзя ответить. Можно попробовать вытягивать последнее сообщение с промптом
    await bot.send_message(chat_id=callback.from_user.id, text=f'prompt = `{rows[0]}`', parse_mode='Markdown')
    await bot.send_message(chat_id=callback.from_user.id, text=f'data = `{data}`', parse_mode='Markdown')
    await bot.send_message(chat_id=callback.from_user.id, text='Менюшка', parse_mode='Markdown', reply_markup=get_ikb())


@dp.callback_query_handler(text='rnd_hr')
async def rnd_hr(callback: types.CallbackQuery) -> None:
    # обновить папку с моделями
    requests.post('http://127.0.0.1:7861/sdapi/v1/refresh-checkpoints', '')
    # вытянуть модели
    response = submit_get('http://127.0.0.1:7861/sdapi/v1/sd-models', '')
    arr = []
    #i = 0
    # заполняем актуальный массив моделей в arr
    for item in response.json():
        arr.append(item['title'])
    await callback.message.edit_text('Ну погнали', reply_markup=get_ikb())
    await bot.send_message(chat_id=callback.from_user.id, text=get_opt(), parse_mode='Markdown')
    # запускаем цикл по списку
    for title in arr:
        #if i < 5:
        # на всякий случай пишем модель в БД. Может надо будет потом убрать, хз
        cur.execute("UPDATE prompts set model = %s where user_id = %s", (title, callback.from_user.id))
        con.commit()
        # меняем модель в памяти
        submit_post('http://127.0.0.1:7861/sdapi/v1/options', {'sd_model_checkpoint': title})
        time.sleep(5)
        data = create_post('gen', 'hr')
        title = title + '\n/stop \n/opt '
        # пока не через media
        with open('dog.png', 'rb') as photo:
            #await callback.message.answer_photo(photo, caption=title, reply_markup=types.ReplyKeyboardRemove())
            print('417 photo')


            #await callback.message.answer_photo(photo, caption=title, reply_markup=types.ReplyKeyboardRemove())
            #await bot.send_message(chat_id=callback.from_user.id, text='проверка', parse_mode='Markdown')
            await bot.send_document(callback.from_user.id, photo, caption=title)
            #TODO photo + title
            #i += 1
    # Для вывода итогов в конце тянем промпт и описание из data
    cur.execute("SELECT prompt from prompts")
    rows = cur.fetchall()
    # callback.reply не сработает, так как на клаву нельзя ответить. Можно попробовать вытягивать последнее сообщение с промптом
    await bot.send_message(chat_id=callback.from_user.id, text=f'prompt = `{rows[0]}`', parse_mode='Markdown')
    await bot.send_message(chat_id=callback.from_user.id, text=f'data = `{data}`', parse_mode='Markdown')
    await bot.send_message(chat_id=callback.from_user.id, text='Менюшка', parse_mode='Markdown', reply_markup=get_ikb())

# Получить все последнии опции с БД текстом
@dp.callback_query_handler(text='get_opt_f')
async def get_opt_f(callback: types.CallbackQuery) -> None:
    await bot.send_message(chat_id=callback.from_user.id, text=get_opt(), reply_markup=get_ikb(), parse_mode='Markdown')

# генератор промптов https://huggingface.co/FredZhang7/distilgpt2-stable-diffusion-v2
@dp.callback_query_handler(text='prompt')
async def prompt(callback: types.CallbackQuery) -> None:
    cur.execute("SELECT prompt from prompts")
    input_ids = tokenizer(cur.fetchall()[0], return_tensors='pt').input_ids
    txt = model.generate(input_ids, do_sample=True, temperature=0.8, top_k=8, max_length=120, num_return_sequences=1,
                            repetition_penalty=1.2, penalty_alpha=0.6, no_repeat_ngram_size=0, early_stopping=True)
    prompt = tokenizer.decode(txt[0], skip_special_tokens=True)
    await bot.send_message(chat_id=callback.from_user.id, text=prompt)

@dp.callback_query_handler(text='random')
async def randomCall(callback: types.CallbackQuery) -> None:
    prompt = get_random_prompt()
    cur.execute("UPDATE prompts set prompt = %s where user_id = %s", (prompt, callback.from_user.id))
    con.commit()

    scale = random.randint(5, 15)
    cur.execute("UPDATE prompts set scale = %s where user_id = %s", (scale, callback.from_user.id))
    con.commit()

    steps = random.randint(15, 60)
    cur.execute("UPDATE prompts set steps = %s where user_id = %s", (steps, callback.from_user.id))
    con.commit()

    # обновить папку с моделями
    requests.post('http://127.0.0.1:7861/sdapi/v1/refresh-checkpoints', '')
    # вытянуть модели
    response = submit_get('http://127.0.0.1:7861/sdapi/v1/sd-models', '')
    arr = []
    for item in response.json():
        arr.append(item['title'])
    model = random.randint(1, len(arr)) - 1
    print(arr[model])
    cur.execute("UPDATE prompts set model = %s where user_id = %s", (arr[model], callback.from_user.id))
    con.commit()
    # меняем модель в памяти
    submit_post('http://127.0.0.1:7861/sdapi/v1/options', {'sd_model_checkpoint': arr[model]})
    time.sleep(5)

    # промпты
    n = random.randint(0, len(arr)-1)
    prompt = data['messages'][n]['text']
    cut_prompt(arr[model], prompt)
    print(prompt)
    cur.execute("UPDATE prompts set prompt = %s where user_id = %s", (prompt, callback.from_user.id))
    con.commit()

    # вытянуть семплеры
    response = submit_get('http://127.0.0.1:7861/sdapi/v1/samplers', '')
    arr = []
    for item in response.json():
        arr.append(item['name'])
    sampler = random.randint(1, len(arr))-1
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
        #await callback.message.delete()
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
         InlineKeyboardButton('gen_hr', callback_data='gen_hr'),
         InlineKeyboardButton('start SD', callback_data='strt')
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
    arr2.append([InlineKeyboardButton('gen', callback_data='gen'),
                 InlineKeyboardButton('gen4', callback_data='gen4'),
                 InlineKeyboardButton('gen_hr', callback_data='gen_hr')
                 ])
    arr2.append([InlineKeyboardButton('rnd', callback_data='rnd'),
                 InlineKeyboardButton('rnd_hr', callback_data='rnd_hr'),
                 InlineKeyboardButton('rnd_rev', callback_data='rnd_rev'),
                 InlineKeyboardButton('rnd_smp', callback_data='rnd_smp')
                 ])
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
    if detect(message.text) == 'ru':
        await bot.send_message(chat_id=message.from_user.id, text='Введите на английском', reply_markup=types.ReplyKeyboardRemove())
    else:
        cur.execute("UPDATE prompts set prompt = %s where user_id = %s", (message.text, message.from_user.id))
        con.commit()
        print("Record inserted successfully")
        await bot.send_message(chat_id=message.from_user.id, text='Выбираем', reply_markup=get_ikb())

if __name__ == '__main__':
    try:
        # Start polling for updates
        # dp.start_polling()
        executor.start_polling(dp, skip_updates=True)
    except Exception as e:
        logging.exception(e)