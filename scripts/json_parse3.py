from aiogram import Bot, Dispatcher, types
from aiogram.utils import executor
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.dispatcher.filters.state import State, StatesGroup
from aiogram.dispatcher import FSMContext

# Инициализация бота и диспетчера
API_TOKEN = "5669797553:AAE3ekwARSYBLnMQrzWxTsbUFefV52gxVeI"  #'900510503:AAG5Xug_JEERhKlf7dpOpzxXcJIzlTbWX1M'
bot = Bot(token=API_TOKEN)
storage = MemoryStorage()
dp = Dispatcher(bot, storage=storage)

# JSON данные
# TODO http://127.0.0.1:7861/openapi.json #/components/schemas/StableDiffusionProcessingTxt2Img
data = {
    "enable_hr": False,
    "prompt": "",
    "seed": -1,
    "override_settings_restore_afterwards": -1,
    "subseed_strength": 0,
}

# https://aiogram-birdi7.readthedocs.io/en/latest/examples/finite_state_machine_example.html
# Dynamically create a new class with the desired attributes
state_classes = {}
for key in data:
    state_classes[key] = State()

# Inherit from the dynamically created class
Form = type("Form", (StatesGroup,), state_classes)


# Команда /get_json для вывода списка параметров
@dp.message_handler(commands=["get_json"])
async def get_json(message: types.Message):
    json_list = [f"/{key} = {value}" for key, value in data.items()]
    json_str = "\n".join(json_list)
    await message.answer(f"JSON параметры:\n{json_str}")


# Ввели любой текст
@dp.message_handler(lambda message: True)
async def change_json(message: types.Message):
    str2 = message.text
    nam = str2.split()[0][1:]
    attrs = dir(Form)
    state_names = [attr for attr in attrs if isinstance(getattr(Form, attr), State)]
    args = message.get_args()
    if nam in state_names:
        if args == "":
            await message.answer("Напиши любое " + nam)
            if nam in state_names:
                await getattr(Form, nam).set()
            else:
                print("Ошибка какая-то")
        else:
            data[nam] = args
            await message.answer(nam + " = " + args + "\n\n/get_json")


# Ввели ответ на change_json
@dp.message_handler(state=Form)
async def answer_handler(message: types.Message, state: FSMContext):
    current_state = await state.get_state()  # Form:команда
    for key, val in data.items():
        if current_state == "Form:" + key:
            data[key] = message.text
            break
    await state.reset_state()
    await message.answer(key + " = " + message.text + "\n\n/get_json")


# Запуск бота
if __name__ == "__main__":
    executor.start_polling(dp, skip_updates=True)
