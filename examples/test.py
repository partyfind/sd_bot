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

print(cut_prompt('KhrushchevkaDiffusion_v10', 'cat in vae'))


"""

import threading

def f():
  threading.Timer(5.0, f).start()  # Перезапуск через 5 секунд
  print("Hello!")

f()



import openai

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