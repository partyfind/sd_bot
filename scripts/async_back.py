# 900510503:AAG5Xug_JEERhKlf7dpOpzxXcJIzlTbWX1M
# https://docs.aiogram.dev/en/latest/
from aiogram import Bot, Dispatcher, types
from aiogram.utils import executor
import asyncio
import subprocess

API_TOKEN = '900510503:AAG5Xug_JEERhKlf7dpOpzxXcJIzlTbWX1M'

bot = Bot(token=API_TOKEN)
dp = Dispatcher(bot)

async def read_pipe(pipe, label, user):
    print('read_pipe')
    # Читаем строки из стандартного вывода скрипта
    while True:
        # Читаем строку из стандартного вывода скрипта
        line = await pipe.readline()
        print(19)
        print(line)

        # Если строка пустая, значит процесс завершился
        if line == b'':
            break

        # Декодируем строку в utf-8 и отправляем ее в чат
        #output = line.decode('utf-8').strip()
        await bot.send_message(user, f'{label}: {line}')

async def get_time(user):
    while True:
        await asyncio.sleep(2)
        #time = subprocess.check_output(['python', 'time.py']).decode('utf-8').strip()
        #process = subprocess.check_output(['python', 'time.py'], stdout=subprocess.PIPE)
        #print(process.stdout)
        #print(f"Этот цикл продолжится бесконечно! {process}")
        process = await asyncio.create_subprocess_exec(
            'python', 'time.py',
            stdout=subprocess.PIPE, stderr=subprocess.PIPE
        )
        print(41)
        print(process.stdout.decode('utf-8'))
        #print(subprocess.PIPE)
        #asyncio.create_task(read_pipe(process.stdout, 'stdout', user))



async def get_info(message: types.Message):
    await message.answer("Это бот")


@dp.message_handler(commands=['time'])
async def start_time(message: types.Message):
    await message.answer("Time started")
    asyncio.create_task(get_time(message.from_user.id))


@dp.message_handler(commands=['info'])
async def start_info(message: types.Message):
    await message.answer("Info started")
    await get_info(message)


if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True)