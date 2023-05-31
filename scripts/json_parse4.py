import json
import logging
from aiogram import Bot, Dispatcher, types
from aiogram.utils import executor
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.dispatcher.filters.state import State, StatesGroup
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters import Text

logging.basicConfig(format="[%(asctime)s] %(levelname)s : %(name)s : %(message)s",
                    level=logging.DEBUG, datefmt="%d-%m-%y %H:%M:%S")

logging.getLogger('aiogram').setLevel(logging.DEBUG)

logger = logging.getLogger(__name__)

# Инициализация бота и диспетчера
API_TOKEN = '5669797553:AAE3ekwARSYBLnMQrzWxTsbUFefV52gxVeI'
bot = Bot(token=API_TOKEN)
storage = MemoryStorage()
dp = Dispatcher(bot, storage=storage)

# JSON данные
data = {
    "enable_hr": 11,
    "ppp": "",
    "sss": -1,
    "over": -1,
    "sub": 0
}

class Form(StatesGroup):
    """
    если напрямки написать enable_hr = State(), то работает
    """
    enable_hr = State()
    def __init__(self):
        global data
        for key in data:
            self.__dict__[key] = State()
        self.data = data

# Команда /get_json для вывода списка параметров
@dp.message_handler(commands=['get_json'])
async def get_json(message: types.Message):
    print(46)
    print(data)
    json_list = [f"/{key} = {value}" for key, value in data.items()]
    json_str = '\n'.join(json_list)
    await message.answer(f"JSON параметры:\n{json_str}")



# Ввели любой текст @dp.message_handler(lambda message: True)
@dp.message_handler(lambda message: True, state='*')
async def change_json(message: types.Message, state: FSMContext):
    print(61)
    async with state.proxy() as data:
        current_state = await state.get_state()
        print(current_state)
        data['enable_hr'] = message.text
    await message.answer("Привет! Напиши любое enable_hr:")
    await Form.enable_hr.set()



# Запуск бота
if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True)