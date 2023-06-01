from aiogram.dispatcher import FSMContext
from aiogram.types import Message
from aiogram.dispatcher.filters import Text
from aiogram.dispatcher.filters.state import State, StatesGroup
import json
from aiogram import Bot, Dispatcher, types
from aiogram.utils import executor
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.dispatcher.filters.state import State, StatesGroup
from aiogram.dispatcher import FSMContext

API_TOKEN = "5669797553:AAE3ekwARSYBLnMQrzWxTsbUFefV52gxVeI"  #'900510503:AAG5Xug_JEERhKlf7dpOpzxXcJIzlTbWX1M'
bot = Bot(token=API_TOKEN)
storage = MemoryStorage()
dp = Dispatcher(bot, storage=storage)


class Form(StatesGroup):
    pass


# Создаем список параметров для формы
params = ["name", "age", "email"]
all_states = []

# Создаем атрибуты объекта Form, названия которых соответствуют параметрам из списка
for param in params:
    setattr(Form, f"{param}_state", State())

    # Добавляем установленные атрибуты в список всех состояний формы
    all_states.append(getattr(Form, f"{param}_state"))


@dp.message_handler(lambda message: True)
async def process_form(message: Message, state: FSMContext):
    # Получаем текущее состояние FSMContext (соответствующее одному из атрибутов Form)
    current_state = await state.get_state()
    print(36)
    print(state)

    if current_state is None:
        # Если текущего состояния нет, переходим в первое состояние Form
        await Form.name_state.set()
        await message.answer("Как вас зовут?")
    else:
        # Используем текущее состояние для выполнения соответствующих действий
        if current_state == Form.name_state:
            # Сохраняем имя пользователя и переходим к следующему состоянию
            name = message.text
            await state.update_data(name=name)
            await Form.age_state.set()
            await message.answer("Сколько вам лет?")
        elif current_state == Form.age_state:
            # Сохраняем возраст пользователя и переходим к следующему состоянию
            age = message.text
            await state.update_data(age=age)
            await Form.email_state.set()
            await message.answer("Какой у вас email?")
        elif current_state == Form.email_state:
            # Сохраняем email пользователя и завершаем диалог
            email = message.text
            data = await state.get_data()

            await message.answer("Спасибо за ваши данные!")
            await state.finish()


# Регистрируем обработчик с фильтром Text и состоянием Form.all_states, чтобы получать все сообщения,
# которые соответствуют любому из состояний Form
dp.register_message_handler(process_form, state=Form.all_states, content_types=Text)

# Запуск бота
if __name__ == "__main__":
    executor.start_polling(dp, skip_updates=True)
