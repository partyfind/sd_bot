import json
from aiogram import Bot, types
from aiogram.dispatcher import Dispatcher
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.dispatcher.filters.state import State, StatesGroup
from aiogram.types import ParseMode
from aiogram.utils import executor
from aiogram.dispatcher import FSMContext

bot_token = '900510503:AAG5Xug_JEERhKlf7dpOpzxXcJIzlTbWX1M'
bot = Bot(token=bot_token)
storage = MemoryStorage()
dp = Dispatcher(bot, storage=storage)

# Пример JSON-объекта
data = {
  "enable_hr": False,
  "prompt": "",
  "styles": [
    "string"
  ],
  "seed": -1,
  "subseed": -1,
  "subseed_strength": 0,
  "seed_resize_from_h": -1,
  "seed_resize_from_w": -1,
  "sampler_name": "string",
  "steps": 50,
  "cfg_scale": 7,
  "width": 512,
  "height": 512,
  "override_settings": {},
  "override_settings_restore_afterwards": True,
  "script_args": [],
  "alwayson_scripts": {}
}

# Обработчик команды /prompt
@dp.message_handler(commands=['override_settings_restore_afterwards'])
async def set_prompt(message: types.Message):
    try:
        # Получаем значение параметра из текста сообщения
        prompt_value = message.text.split()[1]
        # Изменяем значение параметра в JSON-объекте
        data['override_settings_restore_afterwards'] = prompt_value
        print(53)
        print(data)
        # Выводим сообщение об успешном изменении параметра
        await message.reply(f"Значение параметра 'override_settings_restore_afterwards' изменено на '{prompt_value}'")
    except:
        # Если произошла ошибка, выводим сообщение об ошибке
        await message.reply("Не удалось установить значение параметра 'override_settings_restore_afterwards'")

@dp.message_handler(commands=['get_json'])
async def get_json(message: types.Message):
    print('get_json')
    print(data)
    # Сериализуем JSON-объект в строку
    json_text = json.dumps(data, indent=2)
    # Выводим JSON в телеграм
    await message.reply(f"<code>{json_text}</code>", parse_mode=ParseMode.HTML)

@dp.message_handler(commands=['get_keys'])
async def get_keys(message: types.Message, state: FSMContext):
    print('get_keys')
    #TODO добавить динамический вывод команд
    #arr = []
    #for key, value in data.items():
    #    arr.append(data[key])
    #print(arr)
    async with state.proxy() as d:
        print(d)

@dp.message_handler(commands=['reset_json'])
async def reset_json(message: types.Message):
    data2 = {"enable_hr": False,
             "prompt": "",
             "styles": [
               "string"
             ],
             "seed": -1,
             "subseed": -1,
             "subseed_strength": 0,
             "seed_resize_from_h": -1,
             "seed_resize_from_w": -1,
             "sampler_name": "string",
             "steps": 50,
             "cfg_scale": 7,
             "width": 512,
             "height": 512,
             "override_settings": {},
             "override_settings_restore_afterwards": True,
             "script_args": [],
             "alwayson_scripts": {}
            }
    json_text = json.dumps(data, indent=2)
    await message.reply(f"<code>{json_text}</code>", parse_mode=ParseMode.HTML)

if __name__ == '__main__':
    executor.start_polling(dp)