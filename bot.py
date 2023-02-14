"""
This bot is created for the demonstration of a usage of regular keyboards.
"""
import json
import base64
import requests
import logging
import psycopg2

con = psycopg2.connect(
  database="postgres",
  user="postgres",
  password="postgres",
  host="localhost",
  port="5432"
)

from aiogram import Bot, Dispatcher, executor, types


API_TOKEN = '5815882861:AAHVGTfEfozTaU0yRHJEEaYv7gSi4Ag_WBw'

bot = Bot(token=API_TOKEN)
dp = Dispatcher(bot)

inline_btn_1 = InlineKeyboardButton('Первая кнопка!', callback_data='button1')
inline_kb1 = InlineKeyboardMarkup().add(inline_btn_1)

@dp.message_handler()
async def all_msg_handler(message: types.Message):
    button_text = message.text
    # logger.debug('The answer is %r', message.from_user.id)
    cur = con.cursor()
    cur.execute("UPDATE prompts set prompt = %s where user_id = %s", (button_text, message.from_user.id))
    con.commit()
    con.close()

@dp.message_handler(commands=['1'])
async def process_command_1(message: types.Message):
    await message.reply("Первая инлайн кнопка", reply_markup=kb.inline_kb1)

@dp.callback_query_handler(func=lambda c: c.data == 'button1')
async def process_callback_button1(callback_query: types.CallbackQuery):
    await bot.answer_callback_query(callback_query.id)
    await bot.send_message(callback_query.from_user.id, 'Нажата первая кнопка!')

if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True)