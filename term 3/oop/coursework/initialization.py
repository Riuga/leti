import configparser
from telegram import Bot
from telegram.error import InvalidToken


class BotInitialization:
    def __init__(self):
        self.token = None
        self.logs_chat_id = None
        self.load_config()

    def load_config(self):
        """Загружаем конфигурацию из файла."""
        config = configparser.ConfigParser()
        try:
            config.read('config.properties')  # путь к файлу конфигурации
            self.token = config.get('DEFAULT', 'token')
            self.logs_chat_id = int(config.get('DEFAULT', 'logsChannel'))
        except Exception as e:
            print("Unable to load config file.")
            print(e)
            return

        # Проверка валидности токена
        self.validate_token()

    def validate_token(self):
        """Проверка токена на валидность."""
        try:
            bot = Bot(token=self.token)
            bot.get_me()  # если токен неверный, вызовет исключение
        except InvalidToken:
            print("Invalid token.")
            exit(1)

    def get_token(self):
        return self.token

    def set_token(self, token):
        self.token = token
        self.validate_token()

    def get_logs_chat_id(self):
        return self.logs_chat_id

    def set_logs_chat_id(self, report_chat_id):
        self.logs_chat_id = report_chat_id
