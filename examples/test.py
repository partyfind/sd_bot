import json
from googletrans import Translator
import random
arr = []
with open('random.json', encoding='utf-8') as json_file:
    data = json.load(json_file)
    for i in data['messages']:
        if i['text'] != '':
            arr.append(i['text'])
n = random.randint(0, len(arr) - 1)
translator = Translator()
translated = translator.translate(arr[n])
prompt = translated.text
print(prompt)