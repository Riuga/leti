from telegram import Update
from telegram.ext import ContextTypes
from utils.buttons import Buttons


class InputHandler():
    def __init__(self):
        self.buttons = Buttons()

    async def input_handle(self, update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
        user_message = update.message.text

        if not context.user_data.get('user_group_is_valid', False):
            if user_message.isdigit() and len(user_message) == 4:
                context.user_data["group_number"] = user_message
                context.user_data["user_group_is_valid"] = True
                await update.message.reply_text("Спасибо! Номер группы записан")

            elif user_message.isdigit() and len(user_message) != 4:
                await update.message.reply_text("Ошибка! Номер группы должен состоять из 4 цифр")
            else:
                await update.message.reply_text("Ошибка! Номер группы должен состоять из цифр")
        if context.user_data["user_group_is_valid"]:
            await update.message.reply_text("Выберите действие", reply_markup=self.buttons.create_functions_keyboard())
