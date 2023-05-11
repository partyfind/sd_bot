# 900510503:AAG5Xug_JEERhKlf7dpOpzxXcJIzlTbWX1M
# https://docs.aiogram.dev/en/latest/
import asyncio
import subprocess
from aiogram import Bot, Dispatcher, executor, types

bot = Bot(token="900510503:AAG5Xug_JEERhKlf7dpOpzxXcJIzlTbWX1M")
dp = Dispatcher(bot)


@dp.message_handler(commands=['help'])
async def process_help_command(message: types.Message):
    keyboard = types.InlineKeyboardMarkup()
    launch_button = types.InlineKeyboardButton(text="Launch", callback_data="launch")
    stop_button = types.InlineKeyboardButton(text="Stop", callback_data="stop")
    keyboard.row(launch_button, stop_button)
    await bot.send_message(chat_id=message.chat.id, text="Choose an action:", reply_markup=keyboard)


@dp.callback_query_handler(lambda c: c.data == 'launch')
async def process_launch_callback(callback_query: types.CallbackQuery):
    process = subprocess.Popen(["python", "time.py"], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    await bot.answer_callback_query(callback_query.id)
    msg = await bot.send_message(chat_id=callback_query.message.chat.id, text="Launching...")
    print(25)
    while True:
        print(27)
        # Получаем новые сообщения из консоли
        output = process.stdout.readline().decode().strip()
        # Если нет новых сообщений, ждем 1 секунду и продолжаем проверку
        if not output:
            print(30)
            await asyncio.sleep(1)
            continue
        # Отправляем новое сообщение в чат и редактируем предыдущее
        print(output)
        prev_msg = await bot.edit_message_text(chat_id=callback_query.message.chat.id, message_id=msg.message_id,
                                               text=output)
        # Удаляем предыдущее сообщение и продолжаем цикл
        await prev_msg.delete()


@dp.callback_query_handler(lambda c: c.data == 'stop')
async def process_stop_callback(callback_query: types.CallbackQuery):
    print(45)
    subprocess.run(["pkill", "-f", "time.py"])
    keyboard = types.InlineKeyboardMarkup()
    launch_button = types.InlineKeyboardButton(text="Launch", callback_data="launch")
    stop_button = types.InlineKeyboardButton(text="Stop", callback_data="stop")
    keyboard.row(launch_button, stop_button)
    await bot.edit_message_text(chat_id=callback_query.message.chat.id, message_id=callback_query.message.message_id,
                                text="Stopped", reply_markup=keyboard)


if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True)