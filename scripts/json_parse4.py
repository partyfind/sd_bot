import json
from aiogram import Bot, Dispatcher, types
from aiogram.utils import executor
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.dispatcher.filters.state import State, StatesGroup
from aiogram.dispatcher import FSMContext

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
    # если напрямки написать enable_hr = State(), то работает
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
    str = message.text
    if str == '/enable_hr':
        await message.answer('Привет! Напиши любое enable_hr:')
        await Form.enable_hr.set() #  type object 'Form' has no attribute 'enable_hr'
    for key in data:
        # Если ключ json равен вводимой команде И остальное пусто (TODO оптимизировать проверку на пустоту)
        if key == str.split()[0][1:] and str.split()[1:] == []:
            await message.answer('Вы ввели пустую команду' + str + ', введите новое значение ниже либо напишите '+str+' + новое_значение')
        elif key in str: # TODO оптимизировать поиск (починить одинаковость subseed_strength seed)
            substring = str[str.index(key) + len(key):] # вычисляем, до какой строки режем
            # заполняем JSON
            data[key.split()[0][0:]] = substring.split()[0][0:] # /enable_hr = < >текст. Удаляем / и пробел < > через split
            await message.answer('Вы ввели '+str+', теперь '+key+' = '+substring)

@dp.message_handler(state=Form)
async def input_handler(message: types.Message, state: FSMContext):
    # вот сюда ответ не доходит
    print('input_handler')
    async with state.proxy() as data2:
        current_state = await state.get_state() # Form:команда
        for key in data:
            if current_state == 'Form:'+key:
                print(data2[key])
                data2[key] = message.text
        await state.reset_state()
        await message.answer("Спасибос за "+message.text)

# Запуск бота
if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True)