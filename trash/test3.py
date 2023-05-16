import logging
import asyncio

from aiogram import Bot, Dispatcher, types
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.state import State, StatesGroup
from aiogram.types import ParseMode
from aiogram.utils import executor

# Set up logging
logging.basicConfig(level=logging.INFO)

# Create a bot instance and obtain its API token from BotFather
bot = Bot(token='900510503:AAG5Xug_JEERhKlf7dpOpzxXcJIzlTbWX1M')

# Create a Dispatcher instance and plug in a MemoryStorage instance to save FSM state
memory_storage = MemoryStorage()
dp = Dispatcher(bot, storage=memory_storage)

# Define the states of the finite state machine
class GetNumber(StatesGroup):
    waiting_for_number = State()

# Define a command handler to start the bot and enter the FSM state
@dp.message_handler(commands=['start'])
async def cmd_start(message: types.Message):
    await message.reply("Welcome to the number storage bot! Please enter a number:")

    # Enter the waiting_for_number state
    await GetNumber.waiting_for_number.set()

# Define a message handler to retrieve the number input and store it in the FSM context
@dp.message_handler(state=GetNumber.waiting_for_number)
async def process_number_input(message: types.Message, state: FSMContext):
    try:
        number_input = float(message.text)
    except ValueError:
        await message.reply("Sorry, that wasn't a valid number. Please enter a valid number:")
    else:
        # Store the number input in the FSM context and exit the FSM state
        await state.update_data(number=number_input)
        await message.reply(f"Number {number_input:.2f} has been stored successfully!")

        await state.finish()

# Define a command to retrieve the stored number from the FSM context
@dp.message_handler(commands=['get_data'])
async def cmd_get_data(message: types.Message, state: FSMContext):
    data = await state.get_data()
    print(data)
    # Check if "number" key exists in the data dictionary
    if "number" in data:
        number = data["number"]
        await message.reply(f"The stored number is {number:.2f}.")
    else:
        await message.reply("No number has been stored yet.")

if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True)

