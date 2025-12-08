from telegram import Update
from telegram.ext import ContextTypes
from parser.group_data import GroupData
from parser.main_parsing import LessonFetcher
from utils.answer_creator import AnswerCreator
from utils.buttons import Buttons
from utils.time_getter import get_current_week_day, get_current_year, get_current_season


class ButtonHandler:
    def __init__(self):
        self.buttons = Buttons()

    async def button_response(self, update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
        """Handle button responses."""
        query = update.callback_query
        await query.answer()

        group_number = context.user_data['group_number']
        schedule = LessonFetcher.fetch_schedule(group_number, get_current_week_day(), get_current_year(),
                                                get_current_season())

        if not schedule:
            context.user_data["user_group_is_valid"] = False
            await query.edit_message_text(text="Номер группы некорректен, введите новый номер")

        answerCreator = AnswerCreator()
        group_data = GroupData(group=group_number, days={
                               day.name: day for day in schedule})

        if query.data == "near_lesson":

            if schedule:
                await query.edit_message_text(text=answerCreator.create_near_lesson_answer(group_data, ""),
                                              reply_markup=self.buttons.create_functions_keyboard(0))
            else:
                context.user_data["user_group_is_valid"] = False
                await query.edit_message_text(text="Вы ввели неправильный номер группы, введите его еще раз.")

        elif query.data == "day_lessons":

            if schedule:
                await query.edit_message_text(text=answerCreator.create_day_lessons_answer(group_data, ""),
                                              reply_markup=self.buttons.create_functions_keyboard(1))
            else:
                context.user_data["user_group_is_valid"] = False
                await query.edit_message_text(text="Вы ввели неправильный номер группы, введите его еще раз.")

        elif query.data == "tomorrow_lessons":

            if schedule:
                await query.edit_message_text(
                    text=answerCreator.create_tomorrow_lessons_answer(group_number, get_current_year(),
                                                                      get_current_season()),
                    reply_markup=self.buttons.create_functions_keyboard(2))
            else:
                context.user_data["user_group_is_valid"] = False
                await query.edit_message_text(text="Вы ввели неправильный номер группы, введите его еще раз.")

        elif query.data == "week_lessons":

            if schedule:
                await query.edit_message_text(
                    text=answerCreator.create_week_lessons_answer(group_number, get_current_year(),
                                                                  get_current_season()),
                    reply_markup=self.buttons.create_functions_keyboard(3))
            else:
                context.user_data["user_group_is_valid"] = False
                await query.edit_message_text(text="Вы ввели неправильный номер группы, введите его еще раз.")

        elif query.data == "change_group":
            context.user_data["user_group_is_valid"] = False
            await query.edit_message_text(text="Введите новый номер группы")
