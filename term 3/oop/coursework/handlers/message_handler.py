from telegram import Update
from telegram.ext import CallbackContext
import logging

# Enable logging
logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s", level=logging.INFO
)
logger = logging.getLogger(__name__)


class CustomCommandHandler:
    def __init__(self):
        self.commands = {
            "/help": self.show_help,
            "/start": self.start,
            "/report": self.report
        }

    async def handle_command(self, command: str, update: Update, context: CallbackContext):
        """Обрабатывает введенную команду."""
        if command in self.commands:
            # Вызов соответствующего метода
            await self.commands[command](update, context)
        else:
            await context.bot.send_message(chat_id=update.effective_chat.id,
                                           text="Неизвестная команда. Введите /help для просмотра доступных команд.")

    async def show_help(self, update: Update, context: CallbackContext):
        """Показывает доступные команды."""
        help_message = (
            "Доступные команды:\n"
            "/help - просмотр доступных команд\n"
            "/start - перемещение в начало работы бота\n"
            "/report - для написания о проблемах разработчику"
        )
        await context.bot.send_message(chat_id=update.effective_chat.id, text=help_message)

    async def start(self, update: Update, context: CallbackContext):
        user = update.message.from_user
        logger.info("User  %s started the conversation.", user.first_name)
        """Обрабатывает команду /start."""
        welcome_message = "Добро пожаловать! Это начало работы с ботом."
        await context.bot.send_message(chat_id=update.effective_chat.id, text=welcome_message)

        # Запрашиваем номер группы
        await self.ask_group_number(update, context)

    async def ask_group_number(self, update: Update, context: CallbackContext):
        """Запрашивает номер группы у пользователя."""
        await context.bot.send_message(chat_id=update.effective_chat.id, text="Введите номер группы (4 цифры):")
        # Устанавливаем состояние ожидания
        context.user_data['waiting_for_group'] = True

    async def report(self, update: Update, context: CallbackContext):
        """Обрабатывает команду /report."""
        await context.bot.send_message(chat_id=update.effective_chat.id,
                                       text="Опишите проблему, возникшую при использовании бота:")

        # Сохраняем состояние, чтобы ожидать следующего сообщения от пользователя
        context.user_data['waiting_for_issue'] = True
