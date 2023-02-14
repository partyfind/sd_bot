"""
This is a simple example of usage of CallbackData factory
For more comprehensive example see callback_data_factory.py
"""

import asyncio
import logging

from aiogram import Bot, Dispatcher, executor, types
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.contrib.middlewares.logging import LoggingMiddleware
from aiogram.utils.callback_data import CallbackData
from aiogram.utils.exceptions import MessageNotModified

logging.basicConfig(level=logging.INFO)

API_TOKEN = '5815882861:AAHVGTfEfozTaU0yRHJEEaYv7gSi4Ag_WBw'

loop = asyncio.get_event_loop()
bot = Bot(token=API_TOKEN, loop=loop, parse_mode=types.ParseMode.HTML)

storage = MemoryStorage()
dp = Dispatcher(bot, storage=storage)
dp.middleware.setup(LoggingMiddleware())

vote_cb = CallbackData('vote', 'action', 'amount')  # post:<action>:<amount>


def get_keyboard(amount):
    return types.InlineKeyboardMarkup().row(
        types.InlineKeyboardButton('👍', callback_data=vote_cb.new(action='up', amount=amount)),
        types.InlineKeyboardButton('👎', callback_data=vote_cb.new(action='down', amount=amount)))


@dp.message_handler(commands='start')
async def cmd_start(message: types.Message):
    await message.reply('Vote! Now you have 0 votes.', reply_markup=get_keyboard(0))


@dp.callback_query_handler(vote_cb.filter(action='up'))
async def vote_up_cb_handler(query: types.CallbackQuery, callback_data: dict):
    logging.info(callback_data)
    amount = int(callback_data['amount'])
    amount += 1
    await bot.edit_message_text(f'You voted up! Now you have {amount} votes.',
                                query.from_user.id,
                                query.message.message_id,
                                reply_markup=get_keyboard(amount))


@dp.callback_query_handler(vote_cb.filter(action='down'))
async def vote_down_cb_handler(query: types.CallbackQuery, callback_data: dict):
    amount = int(callback_data['amount'])
    amount -= 1
    await bot.edit_message_text(f'You voted down! Now you have {amount} votes.',
                                query.from_user.id,
                                query.message.message_id,
                                reply_markup=get_keyboard(amount))


@dp.errors_handler(exception=MessageNotModified)  # for skipping this exception
async def message_not_modified_handler(update, error):
    return True


if __name__ == '__main__':
    executor.start_polling(dp, loop=loop, skip_updates=True)