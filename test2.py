# 900510503:AAG5Xug_JEERhKlf7dpOpzxXcJIzlTbWX1M
from aiogram import Bot, Dispatcher, types, executor
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.dispatcher.filters import Command

BOT_TOKEN = '900510503:AAG5Xug_JEERhKlf7dpOpzxXcJIzlTbWX1M'
bot = Bot(token=BOT_TOKEN)
dp = Dispatcher(bot, storage=MemoryStorage())

# Обработка команды /start
@dp.message_handler(Command("start"))
async def cmd_start(message: types.Message):
    print('cmd_start')
    await message.answer('Вы ввели старт')

async def set_sd(user_id: int, sd: int):
    await dp.storage.set_data(user=user_id, data='sd', value=sd)

@dp.message_handler(Command("sdon"))
async def sdon(message: types.Message):
    print('sdon')
    handle_start_command(message)
    await message.answer('Вы ввели sdon')


@dp.message_handler(Command("sdoff"))
async def sdoff(message: types.Message):
    print('sdoff')
    handle_stop_command(message)
    await message.answer('Вы ввели sdoff')

@dp.message_handler(Command("stat"))
async def stat(message: types.Message):
    print('stat')
    stats = dp.storage.get_data()
    await message.answer(stats)

def handle_start_command(message):
    set_sd(message.from_user.id, 1) # присваиваем значение 1 переменной SD

def handle_stop_command(message: types.Message):
    set_sd(message.from_user.id, 0) # присваиваем значение 0 переменной SD

if __name__ == '__main__':
    # Запускаем бота
    executor.start_polling(dp, skip_updates=True)