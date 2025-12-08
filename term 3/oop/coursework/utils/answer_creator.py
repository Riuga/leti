from datetime import datetime, timedelta
from parser.group_data import GroupData
from parser.lesson import Lesson
from parser.main_parsing import LessonFetcher


class AnswerCreator:
    def __init__(self):
        self.today = None
        self.sem_start_date = None
        self.day_of_week = None
        self.weeks_between = 0
        self.current_week = 0

        # Словарь для перевода с английских названий дней недели на русские
        self.days_translation = {
            'MONDAY': 'ПОНЕДЕЛЬНИК',
            'TUESDAY': 'ВТОРНИК',
            'WEDNESDAY': 'СРЕДА',
            'THURSDAY': 'ЧЕТВЕРГ',
            'FRIDAY': 'ПЯТНИЦА',
            'SATURDAY': 'СУББОТА',
            'SUNDAY': 'ВОСКРЕСЕНЬЕ'
        }

    def set_locale(self):
        from locale import setlocale, LC_TIME
        setlocale(LC_TIME, 'ru_RU.UTF-8')

    def set_today_settings(self):
        # Получаем текущую дату
        self.today = datetime.now()
        self.set_sem_start_date()
        self.day_of_week = self.today.strftime("%A").upper()

        # Переводим день недели на русский
        self.day_of_week = self.days_translation.get(
            self.day_of_week, self.day_of_week)

        # Количество полных недель между началом семестра и сегодняшним днем
        self.weeks_between = (self.today - self.sem_start_date).days // 7

        # Номер текущей недели (1 для нечетной недели, 2 для четной)
        self.current_week = self.weeks_between % 2 + 1

    def set_sem_start_date(self):
        if self.today.month < 2:
            self.sem_start_date = datetime(self.today.year - 1, 9, 1)
        elif self.today.month > 9:
            self.sem_start_date = datetime(self.today.year, 9, 1)
        else:
            self.sem_start_date = datetime(self.today.year, 2, 3)

    def format_lesson(self, lesson: Lesson) -> str:
        lesson_text = f"{lesson.get_start_time()} - {lesson.get_end_time()} | {lesson.get_subject_type()} {lesson.get_name()}"
        if lesson.get_teacher():
            lesson_text += f", {lesson.get_teacher()}"
        if lesson.get_room():
            lesson_text += f", аудитория: {lesson.get_room()}"
        return lesson_text + "\n"

    def create_day_lessons_answer(self, group_data: GroupData, answer: str) -> str:
        self.set_today_settings()
        day_name = self.day_of_week
        # Получаем объект Day по имени дня недели
        day = group_data.get_days().get(day_name)
        if day:
            answer += f"Расписание на {day.name}:\n\n"

            # Фильтруем уроки по текущей неделе
            lessons_today = [
                lesson for lesson in day.lessons if lesson.get_week() == str(self.current_week)]

            if lessons_today:
                for lesson in lessons_today:
                    answer += self.format_lesson(lesson)
            else:
                answer += f"На {day.name} нет пар.\n\n"
        else:
            answer += f"На {day_name} нет пар.\n\n"

        return answer

    @staticmethod
    def create_week_lessons_answer(group_number, year, season):
        """Создает ответ для расписания на неделю для группы."""
        # Получаем расписание на неделю
        week_schedule = LessonFetcher.fetch_week_schedule(
            group_number, year, season)

        if not week_schedule:
            return f"Расписание на неделю для группы {group_number} не найдено."

        # Получаем текущий день недели и четность недели
        today = datetime.now()
        # Четность недели (0 - нечетная, 1 - четная)
        week_number = (today.isocalendar()[1] + 1) % 2

        # Массив дней недели
        week_days = ["ПОНЕДЕЛЬНИК", "ВТОРНИК", "СРЕДА",
                     "ЧЕТВЕРГ", "ПЯТНИЦА", "СУББОТА", "ВОСКРЕСЕНЬЕ"]

        # Стартуем с формирования ответа
        answer = f"Расписание на неделю для группы {group_number}:\n"

        # Флаг для отслеживания наличия пар
        found_lessons = False

        for i, day_schedule in enumerate(week_schedule):
            # Пропускаем дни, для которых нет расписания
            if day_schedule is None:
                continue

            # Переводим день недели в строку
            day_name = week_days[i]
            answer += f"\n{day_name}:\n"
            day_found = False

            for day in day_schedule:  # Перебираем каждый объект Day
                for lesson in day.lessons:  # Перебираем уроки внутри Day
                    # Проверяем, совпадает ли четность недели с тем, что указано в расписании
                    if int(lesson.week) == week_number + 1:
                        # Добавляем информацию о паре
                        lesson_info = f"\n{lesson.name} ({lesson.subject_type})"
                        lesson_info += f"\n  Преподаватели: {lesson.teacher}"
                        if lesson.second_teacher:
                            lesson_info += f", {lesson.second_teacher}"
                        lesson_info += f"\n  Время: {lesson.start_time} - {lesson.end_time}"
                        lesson_info += f"\n  Аудитория: {lesson.room}\n"
                        answer += lesson_info
                        day_found = True

            # Если на день были найдены пары, то мы добавляем его в общий список
            if day_found:
                found_lessons = True

        # Если не нашли уроков на неделю
        if not found_lessons:
            return f"Расписание на неделю для группы {group_number} не найдено."

        return answer

    @staticmethod
    def create_tomorrow_lessons_answer(group_number, year, season):
        """Создает ответ для расписания на завтра."""
        # Получаем расписание на завтра
        tomorrow_schedule = LessonFetcher.fetch_tomorrow_schedule(
            group_number, year, season)

        if not tomorrow_schedule:
            return f"Расписание на завтра для группы {group_number} не найдено."

        # Получаем дату завтра
        today = datetime.now()
        tomorrow = today + timedelta(days=1)
        # Получаем день недели: 0 = понедельник, 1 = вторник, ..., 6 = воскресенье
        day_of_week = tomorrow.weekday()
        # 0 - для нечетной недели, 1 - для четной недели
        week_number = (today.isocalendar()[1] + 1) % 2

        # Массив дней недели (для соответствия с API)
        week_days = ["MON", "TUE", "WED", "THU", "FRI", "SAT", "SUN"]
        tomorrow_day = week_days[day_of_week]

        # Для отладки выводим информацию о дате и дне недели
        # print(
        #     f"Завтра: {tomorrow.strftime('%d.%m.%Y')}, День недели: {tomorrow.strftime('%A')}, week_number: {week_number}")
        # print(f"Завтра по API ищем день: {tomorrow_day}")  # Отладка

        # Преобразуем данные в строку для удобного отображения
        answer = f"Расписание на завтра ({tomorrow.strftime('%d.%m.%Y')}) для группы {group_number}:\n"
        found_lessons = False

        # Для каждого дня, получаем его информацию
        for day in tomorrow_schedule:
            # print(f"Обработка дня: {day.name}, ищем день: {tomorrow_day}")  # Отладка

            # Приводим дни недели в формат, который понимает API (например, СРЕДА -> WED)
            day_name_map = {
                'ПОНЕДЕЛЬНИК': 'MON',
                'ВТОРНИК': 'TUE',
                'СРЕДА': 'WED',
                'ЧЕТВЕРГ': 'THU',
                'ПЯТНИЦА': 'FRI',
                'СУББОТА': 'SAT',
                'ВОСКРЕСЕНЬЕ': 'SUN'
            }

            api_day_name = day_name_map.get(day.name.upper())

            if api_day_name == tomorrow_day:  # Сравниваем с завтрашним днем по API
                answer += f"{day.name}:\n"
                for lesson in day.lessons:
                    # print(f"Урок: {lesson.name}, неделя: {lesson.week}, week_number: {week_number + 1}")  # Отладка
                    if int(lesson.week) == week_number + 1:  # Учитываем текущую неделю
                        lesson_info = f"\n{lesson.name} ({lesson.subject_type})"
                        lesson_info += f"\n  Преподаватели: {lesson.teacher}"
                        if lesson.second_teacher:
                            lesson_info += f", {lesson.second_teacher}"
                        lesson_info += f"\n  Время: {lesson.start_time} - {lesson.end_time}"
                        lesson_info += f"\n  Аудитория: {lesson.room}\n"
                        answer += lesson_info
                        found_lessons = True

        if not found_lessons:
            return f"На завтра для группы {group_number} пар нет."

        return answer

    def create_near_lesson_answer(self, group_data: GroupData, answer: str) -> str:
        self.set_today_settings()
        time_now = datetime.now()
        current_time = time_now.hour * 3600 + time_now.minute * 60 + time_now.second
        for day_name, day in group_data.get_days().items():
            for lesson in day.lessons:
                if lesson.get_start_time_seconds() < current_time < lesson.get_end_time_seconds():
                    answer += f"Сейчас идет пара: {lesson.get_subject_type()} {lesson.get_name()}\n"
                    if lesson.get_teacher():
                        answer += f"\n  Преподаватель: {lesson.get_teacher()}\n"
                    if lesson.get_room():
                        answer += f"\n  Аудитория: {lesson.get_room()}\n"
                    return answer
        return answer + "Ближайших пар нет.\n"

    def switch_day(self):
        self.today += timedelta(days=1)
        self.day_of_week = self.today.strftime("%A").upper()
        self.weeks_between = (self.today - self.sem_start_date).days // 7
        self.current_week = self.weeks_between % 2 + 1
