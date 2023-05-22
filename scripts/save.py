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
    name = State()
    age = State()
    gender = State()

@dp.message_handler(commands=['start'])
async def start_handler(message: types.Message):
    await message.answer('Привет! Напиши своё имя:')
    await Registration.name.set()

@dp.message_handler(state=Registration.name)
async def name_handler(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        data['name'] = message.text

    await message.answer('Сколько тебе лет?')
    await Registration.next()

@dp.message_handler(lambda message: not message.text.isdigit(), state=Registration.age)
async def age_handler(message: types.Message):
    await message.answer('Пожалуйста, напиши свой возраст цифрами.')
    return

@dp.message_handler(lambda message: message.text.isdigit(), state=Registration.age)
async def age_handler(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        data['age'] = message.text

    await message.answer('Какой у тебя пол?')
    await Registration.next()

@dp.message_handler(lambda message: message.text not in ['Мужской', 'Женский'], state=Registration.gender)
async def gender_handler(message: types.Message):
    await message.answer('Выбери из списка: "Мужской" или "Женский".')
    return

@dp.message_handler(state=Registration.gender)
async def gender_handler(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        data['gender'] = message.text

        await message.answer("Спасибо за регистрацию!\n"
                              f"Ты зарегистрирован как {data['name']}, "
                              f"возраст: {data['age']}, пол: {data['gender']}.")
        # После завершения беседы сбрасываем состояние пользователя:
        await state.reset_state()

@dp.message_handler(commands=['status'])
async def status_handler(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        print(data)
        await bot.send_message(message.chat.id, data['name'])

if __name__ == '__main__':
    asyncio.run(dp.start_polling())