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