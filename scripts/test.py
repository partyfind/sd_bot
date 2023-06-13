import os
import tempfile
from PIL import Image
from aiogram import Bot, types


async def send_small_image(image_path: str, chat_id: int, bot: Bot) -> None:
    with Image.open(image_path) as img:
        # Получаем размеры изображения
        width, height = img.size

        # Определяем коэффициент пропорционального изменения размера
        ratio = min(256 / width, 256 / height)

        # Вычисляем новый размер изображения
        new_size = (round(width * ratio), round(height * ratio))

        # Создаем временный файл для измененного изображения
        with tempfile.NamedTemporaryFile(suffix='.png', delete=False) as temp_file:
            # Изменяем размер изображения и сохраняем его во временный файл
            small_img = img.resize(new_size, resample=Image.LANCZOS)
            small_img.save(temp_file.name)

            # Отправляем изображение в бота
            with open(temp_file.name, 'rb') as small_img_file:
                await
                bot.send_photo(chat_id=chat_id, photo=small_img_file)

            # Удаляем временный файл
            os.remove(temp_file.name)