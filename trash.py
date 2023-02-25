async def create_post():
    txt2img_url = 'http://127.0.0.1:7861/sdapi/v1/txt2img'
    cur.execute("SELECT prompt, steps, width, height, scale, model, negative from prompts")
    rows = cur.fetchall()
    for row in rows:
        #print("user_id =", row[0])
        #print("prompt =", row[1])
        data = {
            'prompt': row[0],
            'steps':  row[1],
            'width':  row[2],
            'height': row[3],
            'cfg_scale': row[4],
            'sd_model_checkpoint':row[5],
            'negative_prompt': row[6]
        }
        prompt = row[0]
    response = submit_post(txt2img_url, data)
    save_encoded_image(response.json()['images'][0], 'dog.png')
    with open('dog.png', 'rb') as photo:
        await message.reply_photo(photo, caption=prompt, reply_markup=types.ReplyKeyboardRemove())


min max
last option


min
512*512
cfg 7
steps 20
generate

max
1024*1024
cfg 15
steps 100
hyres
generate

last
select DB
generate

option
size - text
w h 512*512
512*768
512*1024
768*512
1024*768
768*768
768*1024
scale generate

scale
5 6 7 8 9
10 12 15 17 20
steps generate

steps
20 30 40 50 60 80 100
model generate

model
api
negative generate

negative
enter /negative



@dp.message_handler(commands=["ddd"])
async def cmd_start(message: types.Message):
    change_opt = {'sd_model_checkpoint':'Inkpunk-Diffusion-v2.ckpt [2182245415]'}
    submit_post('http://127.0.0.1:7861/sdapi/v1/options', change_opt)
    data = {
        'prompt': 'Festival, carnival, beautiful scary girls, cyborgs, hyper detailed, very dark lighting, heavy shadows, hyper detailed, vibrant, photo realistic, realistic, dramatic, dark, sharp focus, 8k',
        'steps':  30,
        'width':  512,
        'height': 512,
        'cfg_scale': 12,
        'negative_prompt': ' (bad art), (text title), blurry, frame, Images cut out at the top, left, right, bottom, repetitive, double, lowres, bad anatomy hands, text, error, missing fingers, extra digit, fewer digits, cropped, worst quality, low quality, normal quality, jpeg artifacts, signature, watermark, username, (((uncanny face))), (((ugly face))), ((asymmetrical facial features)), (((wrong anatomy))), (((wrong arms))), (((wrong legs))), ((fused arms)), ((fused legs)), (wrong joints angle), wrong fingers, fused fingers, cross-eyed'
    }
    response = submit_post('http://127.0.0.1:7861/sdapi/v1/txt2img', data)
    save_encoded_image(response.json()['images'][0], 'dog.png')
    #print(response.json())
    with open('dog.png', 'rb') as photo:
        await message.reply_photo(photo, caption='Inkpunk')



@dp.message_handler(commands=["aaa"])
async def cmd_start(message: types.Message):
    change_opt = {'sd_model_checkpoint':'anything-v4.5.ckpt [fbcf965a62]'}
    submit_post('http://127.0.0.1:7861/sdapi/v1/options', change_opt)
    data = {
        'prompt': 'Festival, carnival, beautiful scary girls, cyborgs, hyper detailed, very dark lighting, heavy shadows, hyper detailed, vibrant, photo realistic, realistic, dramatic, dark, sharp focus, 8k',
        'steps':  30,
        'width':  512,
        'height': 512,
        'cfg_scale': 12,
        'negative_prompt': ' (bad art), (text title), blurry, frame, Images cut out at the top, left, right, bottom, repetitive, double, lowres, bad anatomy hands, text, error, missing fingers, extra digit, fewer digits, cropped, worst quality, low quality, normal quality, jpeg artifacts, signature, watermark, username, (((uncanny face))), (((ugly face))), ((asymmetrical facial features)), (((wrong anatomy))), (((wrong arms))), (((wrong legs))), ((fused arms)), ((fused legs)), (wrong joints angle), wrong fingers, fused fingers, cross-eyed'
    }
    response = submit_post('http://127.0.0.1:7861/sdapi/v1/txt2img', data)
    save_encoded_image(response.json()['images'][0], 'dog.png')
    #print(response.json())
    with open('dog.png', 'rb') as photo:
        await message.reply_photo(photo, caption='anything')




@dp.message_handler(commands=['rnd'])
async def send_welcome(message: types.Message):
    randarr()

def randarr():
  threading.Timer(600.0, randarr).start()  # Перезапуск через 600 секунд
  arr = []
  with open('random.json', encoding='utf-8') as json_file:
      data = json.load(json_file)
      for i in data['messages']:
          if i['text'] != '':
              arr.append(i['text'])
  n = math.ceil(random.uniform(0, len(arr) - 1))
  translator = Translator()
  if data['messages'][n]['text'][0][0] != '':
      txt = data['messages'][n]['text']
  else:
      txt = data['messages'][n]['text']
  translated = translator.translate(txt)
  prompt = translated.text
  cur.execute("UPDATE prompts set prompt = %s where user_id = %s", (prompt, 125011869))
  con.commit()

  scale = math.ceil(random.uniform(1, 20))
  cur.execute("UPDATE prompts set scale = %s where user_id = %s", (scale, 125011869))
  con.commit()

  steps = math.ceil(random.uniform(20, 60))
  # steps = 20
  cur.execute("UPDATE prompts set steps = %s where user_id = %s", (steps, 125011869))
  con.commit()

  # обновить папку с моделями
  requests.post('http://127.0.0.1:7861/sdapi/v1/refresh-checkpoints', '')
  # вытянуть модели
  response = submit_get('http://127.0.0.1:7861/sdapi/v1/sd-models', '')
  #result = [x['title'] for x in response.json() if x["model_name"] == s]
  arr = []
  for item in response.json():
      arr.append(item['title'])
  model = math.ceil(random.uniform(1, len(arr))) - 1
  print(arr[model])
  # меняем модель в памяти
  submit_post('http://127.0.0.1:7861/sdapi/v1/options', {'sd_model_checkpoint': arr[model]})
  time.sleep(5)
  cur.execute("UPDATE prompts set model = %s where user_id = %s", (arr[model], 125011869))
  con.commit()

  # вытянуть семплеры
  response = submit_get('http://127.0.0.1:7861/sdapi/v1/samplers', '')
  arr = []
  for item in response.json():
      arr.append(item['name'])
  sampler = math.ceil(random.uniform(1, len(arr))) - 1
  cur.execute("UPDATE prompts set sampler = %s where user_id = %s", (arr[sampler], 125011869))
  con.commit()

  print("new prompt")
  data = create_post('gen4', '')
  media = types.MediaGroup()
  media.attach_photo(types.InputFile('dog.png'), json.dumps(data))
  media.attach_photo(types.InputFile('dog2.png'), json.dumps(data))
  media.attach_photo(types.InputFile('dog3.png'), json.dumps(data))
  media.attach_photo(types.InputFile('dog4.png'), json.dumps(data))
  #await callback.message.delete()
  bot.send_media_group(125011869, media=media)
  #await bot.send_message(chat_id=callback.from_user.id, text='Выбираем заново', reply_markup=get_ikb())
  bot.send_message(chat_id=125011869, text=prompt)