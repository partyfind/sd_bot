import json
from aiogram import Bot, Dispatcher, types
from aiogram.utils import executor
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.dispatcher.filters.state import State, StatesGroup
from aiogram.dispatcher import FSMContext

# Инициализация бота и диспетчера
API_TOKEN = '900510503:AAG5Xug_JEERhKlf7dpOpzxXcJIzlTbWX1M'
bot = Bot(token=API_TOKEN)
storage = MemoryStorage()
dp = Dispatcher(bot, storage=storage)

# JSON данные
# TODO http://127.0.0.1:7861/openapi.json #/components/schemas/StableDiffusionProcessingTxt2Img
data = {
    "enable_hr": False,
    "prompt": "",
    "seed": -1,
    "override_settings_restore_afterwards": -1,
    "subseed_strength": 0
}

#TODO оптимизировать
def get_json_keys():
    arr = []
    for key, val in data.items():
        arr.append(key)
    return arr

# https://aiogram-birdi7.readthedocs.io/en/latest/examples/finite_state_machine_example.html
"""class Form(StatesGroup):
    text = State()
    num = State()
for key in data:
    print(key)
    setattr(Form, key, State())"""
class Form(StatesGroup):
    def __init__(self, data):
        for key in data:
            setattr(self, key, State())
        self.data = data

# Команда /get_json для вывода списка параметров
@dp.message_handler(commands=['get_json'])
async def get_json(message: types.Message):
    json_list = [f"/{key} = {value}" for key, value in data.items()]
    json_str = '\n'.join(json_list)
    await message.answer(f"JSON параметры:\n{json_str}")

# Ввели любой текст
@dp.message_handler(lambda message: True)
async def change_json(message: types.Message):
    print(5444)
    print(Form)
    str = message.text
    if str == '/text':
        await message.answer('Привет! Напиши любой текст:')
        await Form.text.set()
    elif str == '/num':
        await message.answer('Привет! Напиши любое число:')
        await Form.num.set()
    elif str == '/enable_hr':
        await message.answer('Привет! Напиши любое enable_hr:')
        await Form.enable_hr.set()
"""    for key in data:
        # Если ключ json равен вводимой команде И остальное пусто (TODO оптимизировать проверку на пустоту)
        if key == str.split()[0][1:] and str.split()[1:] == []:
            await message.answer('Вы ввели пустую команду' + str + ', введите новое значение ниже либо напишите '+str+' + новое_значение')
        elif key in str: # TODO оптимизировать поиск (починить одинаковость subseed_strength seed)
            substring = str[str.index(key) + len(key):] # вычисляем, до какой строки режем
            data[key.split()[0][0:]] = substring.split()[0][0:] # /prompt = < >текст. Удаляем / и пробел < > через split
            print(data)
            await message.answer('Вы ввели '+str+', теперь '+key+' = '+substring)"""

@dp.message_handler(state=Form)
async def gender_handler(message: types.Message, state: FSMContext):
    print(63)
    async with state.proxy() as data2:
        current_state = await state.get_state() # Form:команда
        print(65)
        print(data2)
        print(68)
        print(state)
        print(current_state)
        for key in data:
            if current_state == 'Form:'+key:
                print(data2[key])
                data2[key] = message.text
        #if current_state == 'Form:num':
        #    print('nummm')
        #if current_state == 'Form:text':
        #    print('texttt')
        await state.reset_state()
        #data2['text'] = message.text
        await message.answer("Спасибос за "+message.text)
        # После завершения беседы сбрасываем состояние пользователя:
        #await state.reset_state()

"""@dp.message_handler(state=Form.text)
async def gender_handler(message: types.Message, state: FSMContext):
    async with state.proxy() as data2:
        print(data2)
        data2['text'] = message.text
        await message.answer("Спасибо за текст!\n"
                              f" text {data2['text']}, ")
        # После завершения беседы сбрасываем состояние пользователя:
        await state.reset_state()

@dp.message_handler(state=Form.num)
async def gender_handler(message: types.Message, state: FSMContext):
    async with state.proxy() as data2:
        print(data2)
        data2['num'] = message.text
        await message.answer("Спасибо за число!\n"
                              f" num {data2['num']}, ")
        # После завершения беседы сбрасываем состояние пользователя:
        await state.reset_state()"""

# Запуск бота
if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True)