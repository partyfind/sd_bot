import json
from aiogram import Bot, Dispatcher, types
from aiogram.dispatcher import filters
from aiogram.utils import executor
import json
from aiogram import Bot, Dispatcher, types
from aiogram.types import ParseMode
from aiogram.utils import executor
from aiogram.dispatcher.filters import Command
from aiogram.dispatcher.filters.state import State, StatesGroup
from aiogram.dispatcher import FSMContext

# Инициализация бота и диспетчера
API_TOKEN = '900510503:AAG5Xug_JEERhKlf7dpOpzxXcJIzlTbWX1M'
bot = Bot(token=API_TOKEN)
dp = Dispatcher(bot)

class Registration(StatesGroup):
    enable_hr = State()
    prompt = State()
    seed = State()
    override_settings_restore_afterwards = State()
    subseed_strength = State()

# JSON данные
data = {
    "enable_hr": False,
    "prompt": "",
    "seed": -1,
    "override_settings_restore_afterwards": -1,
    "subseed_strength": 0
}

# Команда /get_json для вывода списка параметров
@dp.message_handler(commands=['get_json'])
async def get_json(message: types.Message):
    json_list = [f"/{key} = {value}" for key, value in data.items()]
    json_str = '\n'.join(json_list)
    await message.answer(f"JSON параметры:\n{json_str}")

# Функция для проверки типа значения по ключу
def check_value(key, value):
    if isinstance(value, bool) and key != "enable_hr":
        return False
    elif isinstance(value, int) and key != "seed" and key != "override_settings_restore_afterwards" and key != "subseed_strength":
        return False
    elif isinstance(value, str) and key != "prompt":
        return False
    return True

# Обработка введенных значений для изменения JSON
@dp.message_handler(lambda message: True, state=Registration)
async def change_json(message: types.Message, state: FSMContext):
    print('__________')
    print(message)
    print(message.text)
    async with state.proxy() as data2:
        print(data2)
    command = message.text #.get_command()
    key = command#[1:]
    print(data.keys())

    # Если сообщение не начинается с /
    #if not command.startswith("/") and key not in data.keys():
    #    print(68)
    #    return

    # Определение типа введенного значения и запись в JSON
    value = message.text[len(command) + 1:]
    """    
        if value.lower() == "true":
            data[key] = True
        elif value.lower() == "false":
            data[key] = False
        elif value.isnumeric():
            data[key] = int(value)
        else:
            data[key] = value"""
    data[value] = key

    await message.answer(f"Значение {data[key]} изменилось на {command}")


# Обработка команд для изменения значений в JSON
@dp.message_handler(filters.Command(commands=['enable_hr', 'prompt', 'seed', 'override_settings_restore_afterwards', 'subseed_strength']))
async def handle_command(message: types.Message):
    print(54)
    command = message.get_command()
    print(command)
    key = command[1:]
    value = data[key]

    # Определение типа значения по ключу и вывод предложения для изменения
    if check_value(key, value):
        await message.answer(f"Вы ввели {command}, у неё значение {value}, какое новое значение?")
        #await message.answer('Привет! Напиши своё имя:')
        #await Registration.command.set()
    else:
        await message.answer("Ошибка! Невозможно изменить значение данного параметра.")

# Запуск бота
if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True)