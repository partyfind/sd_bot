import aiogram
import asyncio
import subprocess
import concurrent.futures
from datetime import datetime

bot = aiogram.Bot('900510503:AAG5Xug_JEERhKlf7dpOpzxXcJIzlTbWX1M')
dp = aiogram.Dispatcher(bot)
process = None

# Список запущенных задач
tasks = []

# Функция для запуска фонового скрипта
async def run_launch():
    global process
    if not process:
        process = subprocess.Popen(['python', 'launch.py'])
        await asyncio.get_running_loop().run_in_executor(None, process.communicate)

# Обработчик команды /launch
@dp.message_handler(commands='launch')
async def launch_handler(message: aiogram.types.Message):
    #await message.answer('Запущен фоновый скрипт')
    #script_task = asyncio.create_task(run_launch(), name='script')
    #tasks.append(script_task)
    #await asyncio.gather(script_task)
    asyncio.create_task(run_launch(), name='launch')


# Обработчик команды /stop
@dp.message_handler(commands='stop')
async def stop_handler(message: aiogram.types.Message):
    global process
    if process:
        # Нужно очищать?
        for task in tasks:
            if task.get_name() == 'launch':
                print(51)
                task.cancel()
                tasks.remove(task)
        print('stop_process sd')
        process.terminate()
        process = None
    await message.answer('Фоновый скрипт остановлен')



# Обработчик команды /time
@dp.message_handler(commands='time')
async def time_handler(message: aiogram.types.Message):
    # Выводим текущее системное время
    await message.answer(str(datetime.now()))

if __name__ == '__main__':
    aiogram.executor.start_polling(dp)