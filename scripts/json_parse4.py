import json
from aiogram import Bot, Dispatcher, types
from aiogram.utils import executor
from aiogram.contrib.fsm_storage.memory import MemoryStorage

# Инициализация бота и диспетчера
API_TOKEN = '900510503:AAG5Xug_JEERhKlf7dpOpzxXcJIzlTbWX1M'
bot = Bot(token=API_TOKEN)
storage = MemoryStorage()
dp = Dispatcher(bot, storage=storage)

# JSON данные
data = {
    "enable_hr": False,
    "prompt": "222",
    "seed": -1,
    "override_settings_restore_afterwards": -1,
    "subseed_strength": 0
}
ret = ''

# Команда /get_json для вывода списка параметров
@dp.message_handler(commands=['get_json'])
async def get_json(message: types.Message):
    json_list = [f"/{key} = {value}" for key, value in data.items()]
    json_str = '\n'.join(json_list)
    await message.answer(f"JSON параметры:\n{json_str}")

# Ввели любой текст
@dp.message_handler(lambda message: True)
async def change_json(message: types.Message):
    print('change_json')
    str = message.text
    for key, value in data.items():
        if str[1:] in data:
            print(str[1:]+' = '+data[str[1:]])

# Запуск бота
if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True)