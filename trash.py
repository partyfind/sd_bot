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