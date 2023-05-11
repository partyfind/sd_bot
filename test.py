# 900510503:AAG5Xug_JEERhKlf7dpOpzxXcJIzlTbWX1M
# https://docs.aiogram.dev/en/latest/
import subprocess
from aiogram import Bot, Dispatcher, types
from aiogram.types import ReplyKeyboardMarkup, InlineKeyboardMarkup, InlineKeyboardButton, InputFile
from aiogram.utils import executor

bot_token = '900510503:AAG5Xug_JEERhKlf7dpOpzxXcJIzlTbWX1M'  # замените '<TOKEN>' на ваш токен
bot = Bot(token=bot_token)
dp = Dispatcher(bot)

def getOpt() -> InlineKeyboardMarkup:
    opt = InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton('opt', callback_data='opt'),
         InlineKeyboardButton('gen', callback_data='gen')]
    ])
    return opt

# Обработка команды /help
@dp.message_handler(commands=['help'])
async def cmd_help(callback: types.CallbackQuery) -> None:
    print('cmd_help')
    await bot.send_message(chat_id=callback.from_user.id,
                           text='Бот для генерации картинок и промптов. \nКоманды:\n /opt - опции \n /gen - вид генерации',
                           reply_markup=getOpt(),
                           parse_mode='Markdown')

async def send_error_message(callback, error_message):
    try:
        #await bot.send_message(callback.from_user.id, f'Ошибка: {error_message}')
        print('send_error_message')
        await callback.message.edit_text(error_message)
    except Exception as e:
        print(f"Ошибка отправки сообщения в Telegram: {e}")

@dp.callback_query_handler(text='opt')
async def startSD(callback: types.CallbackQuery) -> None:
    print('startSD')
    process = subprocess.Popen(['python', 'launch.py', '--nowebui', '--xformers'], stderr=subprocess.PIPE)
    while True:
        await callback.message.edit_text(process.stderr.readline().decode().strip())

if __name__ == '__main__':
    executor.start_polling(dp)