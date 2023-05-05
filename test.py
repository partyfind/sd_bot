#900510503:AAG5Xug_JEERhKlf7dpOpzxXcJIzlTbWX1M
from telegram import Update
from telegram.ext import Updater, CommandHandler, CallbackContext
import time
import sys

# Токен вашего Telegram бота
TOKEN = "900510503:AAG5Xug_JEERhKlf7dpOpzxXcJIzlTbWX1M"

# ID чата, куда будут отправляться сообщения
CHAT_ID = "125011869"

# Функция обработчик команды старта
def start(update: Update, context: CallbackContext):
    # Отправляем сообщение со статусом "In progress"
    message = context.bot.send_message(chat_id=CHAT_ID, text="In progress...")
    # Запускаем длительный процесс
    for i in range(10):
        time.sleep(1)  # Длительный процесс
        # Обновляем сообщение с прогрессом выполнения
        context.bot.edit_message_text(chat_id=CHAT_ID,
                                      message_id=message.message_id,
                                      text=f"Выполнено: {i+1}/10")
    # Отправляем сообщение с результатом выполнения
    context.bot.edit_message_text(chat_id=CHAT_ID,
                                  message_id=message.message_id,
                                  text="Готово!")
    # Завершаем выполнение скрипта
    sys.exit()

def main():
    # Создаем объект updater и привязываем его к Telegram боту
    updater = Updater(TOKEN) #, use_context=True
    # Создаем диспетчер для регистрации обработчиков команд
    dispatcher = updater.dispatcher
    # Регистрируем обработчик команды старта
    dispatcher.add_handler(CommandHandler("start", start))
    # Запускаем бота
    updater.start_polling()
    # Ожидаем остановки бота
    updater.idle()

if __name__ == '__main__':
    main()