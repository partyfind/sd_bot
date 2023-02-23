import threading

def f():
  threading.Timer(600.0, f).start()  # Перезапуск через 5 секунд
  print("Hello!")

f()
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