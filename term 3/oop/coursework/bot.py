import logging
import configparser
from telegram import Bot, Update
from telegram.ext import Application, CommandHandler, MessageHandler, CallbackQueryHandler
from handlers import button_handler
from handlers.button_handler import ButtonHandler
from handlers.input_handler import InputHandler
from handlers.message_handler import CustomCommandHandler

# Настройка логирования
logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s", level=logging.INFO
)
logger = logging.getLogger(__name__)


# Чтение конфигурации из файла config.ini
config = configparser.ConfigParser()
config.read('config.ini')

# Извлекаем значения из секции DEFAULT
BOT_TOKEN = config['DEFAULT']['token']


def main():
    # Инициализация бота
    bot = Bot(token=BOT_TOKEN)

    # Создание application для получения обновлений (вместо Updater в новой версии)
    application = Application.builder().token(BOT_TOKEN).build()

    # Создаем экземпляры обработчиков
    global command_handler
    global input_handler
    global button_handler
    command_handler = CustomCommandHandler()
    input_handler = InputHandler()
    button_handler = ButtonHandler()

    # Добавление обработчиков команд
    application.add_handler(CommandHandler("start", command_handler.start))
    application.add_handler(CommandHandler("help", command_handler.show_help))
    application.add_handler(CommandHandler("report", command_handler.report))

    # Обработка текстовых сообщений
    # Обрабатываем все текстовые сообщения
    application.add_handler(MessageHandler(None, input_handler.input_handle))

    # Обработка нажатий на кнопки
    application.add_handler(CallbackQueryHandler(
        button_handler.button_response))

    # Запуск бота
    application.run_polling(allowed_updates=Update.ALL_TYPES)


if __name__ == '__main__':
    main()
