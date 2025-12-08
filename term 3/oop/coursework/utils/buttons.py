from telegram import InlineKeyboardButton, InlineKeyboardMarkup


class Buttons:
    def create_functions_keyboard(self, button_to_delete=None):
        """Создает клавиатуру с функциями."""
        if button_to_delete is None:
            keyboard = [
                [
                    InlineKeyboardButton(
                        "Следующая пара", callback_data="near_lesson"),
                    InlineKeyboardButton(
                        "Расписание на день", callback_data="day_lessons")
                ],
                [
                    InlineKeyboardButton(
                        "Расписание на завтра", callback_data="tomorrow_lessons"),
                    InlineKeyboardButton(
                        "Расписание на неделю", callback_data="week_lessons")
                ],
                [
                    InlineKeyboardButton(
                        "Поменять группу", callback_data="change_group")
                ]
            ]
        else:
            buttons_name = [["Следующая пара", "near_lesson"], ["Расписание на день", "day_lessons"],
                            ["Расписание на завтра", "tomorrow_lessons"], [
                                "Расписание на неделю", "week_lessons"],
                            ["Поменять группу", "change_group"]]
            buttons_name.pop(button_to_delete)

            keyboard = [
                [
                    InlineKeyboardButton(
                        buttons_name[0][0], callback_data=buttons_name[0][1]),
                    InlineKeyboardButton(
                        buttons_name[1][0], callback_data=buttons_name[1][1])
                ],
                [
                    InlineKeyboardButton(
                        buttons_name[2][0], callback_data=buttons_name[2][1]),
                    InlineKeyboardButton(
                        buttons_name[3][0], callback_data=buttons_name[3][1])
                ]
            ]

        return InlineKeyboardMarkup(keyboard)
