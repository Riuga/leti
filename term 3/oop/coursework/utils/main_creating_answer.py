from parser.main_parsing import LessonFetcher
from answer_creator import AnswerCreator
from parser.group_data import GroupData
from utils.time_getter import get_current_week_day, get_current_year, get_current_season

group_number = 3390
schedule = LessonFetcher.fetch_schedule(
    group_number, get_current_week_day(), get_current_year(), get_current_season())

if schedule:
    group_data = GroupData(group="3390", days={
                           day.name: day for day in schedule})
    answer_creator = AnswerCreator()

    # # Создаем ответ для расписания на сегодня
    # print(answer_creator.create_day_lessons_answer(group_data, ""))

    # # # Создаем ответ для расписания на завтра
    print(AnswerCreator.create_tomorrow_lessons_answer(
        group_number, get_current_year(), get_current_season()))
    #
    # # # Создаем ответ для расписания на всю неделю
    # print(AnswerCreator.create_week_lessons_answer(group_number, get_current_year(), get_current_season()))
    #
    # # # # Создаем ответ для ближайшей пары
    # print(answer_creator.create_near_lesson_answer(group_data, ""))
else:
    print(schedule)
    print(f"Не удалось получить расписание для группы {group_number}.")
