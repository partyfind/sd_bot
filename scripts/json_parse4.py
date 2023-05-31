import asyncio
import json
import logging

from aiogram import Bot, Dispatcher, types
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.state import State, StatesGroup
from aiogram.utils import executor

# Настройка логгера
logging.basicConfig(format="[%(asctime)s] %(levelname)s : %(name)s : %(message)s",
                    level=logging.DEBUG, datefmt="%d-%m-%y %H:%M:%S")

logging.getLogger('aiogram').setLevel(logging.DEBUG)

logger = logging.getLogger(__name__)

# Инициализация бота и диспетчера
API_TOKEN = '5669797553:AAE3ekwARSYBLnMQrzWxTsbUFefV52gxVeI'#"900510503:AAG5Xug_JEERhKlf7dpOpzxXcJIzlTbWX1M"
bot = Bot(token=API_TOKEN)
storage = MemoryStorage()
dp = Dispatcher(bot, storage=storage)

# JSON данные
data = {"enable_hr": 11, "ppp": "", "sss": -1, "over": -1, "sub": 0}


class Form(StatesGroup):
    """
    если напрямки написать enable_hr = State(), то работает
    """

    def __init__(self):
        global data
        for key in data:
            self.__dict__[key] = State()
        self.data = data


@dp.message_handler(commands=["get_json"])
async def get_json(message: types.Message):
    """
    Команда /get_json для вывода списка параметров
    :param message:
    :return:
    """
    # json_list = [f"/{key} = {value}" for key, value in data.items()]
    # json_str = '\n'.join(json_list)
    json_str = json.dumps(data)
    await message.answer(f"JSON параметры:\n{json_str}")


@dp.message_handler(lambda message: True)
async def change_json(message: types.Message):
    """
    Ввели любой текст
    :param message:
    :return:
    """
    text_line = message.text
    if text_line == "/enable_hr":
        await message.answer("Привет! Напиши любое enable_hr:")
        try:
            await Form.enable_hr.set()
        except Exception as e:
            logging.error(f"change json error: {e}")
            pass
            # type object 'Form' has no attribute 'enable_hr'

    for key in data:
        #  Если ключ json равен вводимой команде И остальное пусто
        #  (TODO оптимизировать проверку на пустоту)
        if key == text_line.split()[0][1:] and text_line.split()[1:] == []:
            await message.answer(
                f"Вы ввели пустую команду{text_line}, "
                f"введите новое значение ниже либо напишите {text_line} новое_значение"
            )
        elif key in text_line:
            # TODO оптимизировать поиск (починить одинаковость subseed_strength seed)
            substring = text_line[text_line.index(key) + len(key):]
            # вычисляем, до какой строки режем
            # заполняем JSON
            data[key.split()[0][0:]] = substring.split()[0][0:]
            # /enable_hr = < >текст. Удаляем / и пробел < > через split
            await message.answer(f"Вы ввели {text_line}, теперь {key} = {substring}")


@dp.message_handler(state=Form)
async def input_handler(message: types.Message, state: FSMContext):
    """
    вот сюда ответ не доходит
    :param message:
    :param state:
    :return:
    """
    logging.info("input_handler")
    async with state.proxy() as data2:
        current_state = await state.get_state()
        # Form:команда
        for key in data:
            if current_state == f"Form: {key}":
                logging.info(data2[key])
                data2[key] = message.text
        await state.reset_state()
        await message.answer(f"Спасибос за {message.text}")


if __name__ == "__main__":
    """
    Запуск бота
    """
    logging.info("starting bot")
    loop = asyncio.new_event_loop()
    executor.start_polling(dp, loop=loop, skip_updates=True)
