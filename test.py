# 900510503:AAG5Xug_JEERhKlf7dpOpzxXcJIzlTbWX1M
# https://docs.aiogram.dev/en/latest/
from aiogram import Bot, Dispatcher, types, executor
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.dispatcher.filters import Command

# API токен бота
token = '900510503:AAG5Xug_JEERhKlf7dpOpzxXcJIzlTbWX1M'

# Инициализируем бота и диспетчер
bot = Bot(token=token, parse_mode=types.ParseMode.MARKDOWN_V2)
storage = MemoryStorage()
dp = Dispatcher(bot, storage=storage)

# Обработка команды /start
@dp.message_handler(Command("start"))
async def cmd_start(message: types.Message):
    print('cmd_start')
    storage.set_data('time', '20')
    await message.answer('Вы ввели старт')

# Обработка команды /help
@dp.message_handler(Command("help"))
async def cmd_help(callback: types.CallbackQuery) -> None:
    print('cmd_help')
    await bot.send_message(chat_id=callback.from_user.id,
                           text='Бот для генерации картинок и промптов. \nКоманды:\n /opt - опции \n /gen - вид генерации',
                           parse_mode='Markdown')

# menu Options
def menuOpt() -> InlineKeyboardMarkup:
    m = InlineKeyboardMarkup(inline_keyboard=[
          [InlineKeyboardButton('start SD', callback_data='startSD'),
           InlineKeyboardButton('stop SD',  callback_data='stopSD')]
        ])
    return m

# Нажали opt
@dp.message_handler(Command("opt"))
async def get_opt(callback: types.CallbackQuery) -> None:
    print('get_opt')
    await bot.send_message(chat_id=callback.from_user.id, text='текст над opt', reply_markup=menuOpt(), parse_mode='Markdown')

if __name__ == '__main__':
    # Запускаем бота
    executor.start_polling(dp, skip_updates=True)