import json
import random
import math
arr = []
with open('random.json', encoding='utf-8') as json_file:
    data = json.load(json_file)
    for i in data['messages']:
        if i['text'] != '':
            arr.append(i['text'])
n = math.ceil(random.uniform(0, len(arr)-1))
print(arr[0])
print(arr[1])
print(arr[2])
#print(arr[3])
print(n)
print(arr[n])

"""import openai

openai.Completion.create(
  engine="davinci",
  prompt="Make a list of astronomical observatories:"
)

import openai
openai.api_key = API_KEY
prompt = "Say this is a test"
response = openai.Completion.create(
    engine="text-davinci-001", prompt=prompt, max_tokens=6
)
print(response)

import googletrans
#print(googletrans.LANGUAGES)
from googletrans import Translator
result = Translator.translate('Привет')
print(result.src)
print(result.dest)
print(result.origin)
print(result.text)
print(result.pronunciation)

from googletrans import Translator

translator = Translator()
translated = translator.translate('Words check')

print(translated.text)
"""