import asyncio
from aiogram import Bot, Dispatcher, types
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.state import State, StatesGroup

TOKEN = '900510503:AAG5Xug_JEERhKlf7dpOpzxXcJIzlTbWX1M'

bot = Bot(token=TOKEN)
storage = MemoryStorage()
dp = Dispatcher(bot, storage=storage)

class Registration(StatesGroup):
    random_num = State()
    random_text = State()

@dp.message_handler(commands=['start'])
async def start_handler(message: types.Message):
    await message.answer('Привет! Напиши рандомное число:')
    await Registration.random_num.set()

# Registration.random_num - ловит сообщение в телеге
@dp.message_handler(state=Registration.random_num)
async def name_handler(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        data['random_num'] = message.text
    await message.answer('Введи случайный текст')
    await Registration.next()

@dp.message_handler(state=Registration.random_text)
async def gender_handler(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        data['random_text'] = message.text

        await message.answer("Спасибо за регистрацию!\n"
                              f" random_num {data['random_num']}, "
                              f"random_text: {data['random_text']}.")
        # После завершения беседы сбрасываем состояние пользователя:
        await state.reset_state()

@dp.message_handler(commands=['random_num'])
@dp.message_handler(commands=['random_text'])
async def status_handler(message: types.Message, state: FSMContext):
    print(message)
    #if message.text == '':

    async with state.proxy() as data:
        print(data)
        await bot.send_message(message.chat.id, data[message.text.replace('/', '')])

if __name__ == '__main__':
    asyncio.run(dp.start_polling())