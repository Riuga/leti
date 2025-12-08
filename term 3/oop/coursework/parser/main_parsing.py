from datetime import datetime, timedelta

import requests
from parser.day import Day
from parser.lesson import Lesson


class LessonFetcher:
    @staticmethod
    def fetch_schedule(group_number, week_day, year, season):
        url = (
            f"https://digital.etu.ru/api/mobile/schedule?"
            f"groupNumber={group_number}&weekDay={week_day}&joinWeeks=false"
            f"&year={year}&season={season}"
        )
        # print(f"Запрос к API: {url}")

        try:
            response = requests.get(url)
            # print(f"Код ответа: {response.status_code}")

            if response.status_code == 200:
                data = response.json()
                # print(f"Полный ответ API: {data}")

                # Проверяем наличие группы в ответе
                group_data = data.get(str(group_number))
                if not group_data:
                    print(f"Группа {group_number} отсутствует в ответе.")
                    return None

                # Проверяем наличие дней
                days_data = group_data.get('days')
                if not days_data:
                    print(f"Дни отсутствуют для группы {group_number}.")
                    return None

                # Преобразуем данные в объекты Day
                days = []
                for day_key, day_value in days_data.items():
                    day = Day(
                        name=day_value['name'],
                        lessons=[
                            Lesson(
                                teacher=lesson.get('teacher'),
                                second_teacher=lesson.get('second_teacher'),
                                subject_type=lesson.get('subjectType'),
                                week=lesson.get('week'),
                                name=lesson.get('name'),
                                start_time=lesson.get('start_time'),
                                end_time=lesson.get('end_time'),
                                start_time_seconds=lesson.get(
                                    'start_time_seconds'),
                                end_time_seconds=lesson.get(
                                    'end_time_seconds'),
                                room=lesson.get('room'),
                                comment=lesson.get('comment'),
                                form=lesson.get('form'),
                                temp_changes=lesson.get('temp_changes', []),
                                url=lesson.get('url')
                            )
                            for lesson in day_value.get('lessons', [])
                        ]
                    )
                    days.append(day)
                return days
            else:
                print(
                    f"Ошибка при запросе API: Код ответа {response.status_code}")
                return None
        except Exception as e:
            print(f"Ошибка при выполнении запроса: {e}")
            return None

    @staticmethod
    def fetch_week_schedule(group_number, year, season):
        week_days = ["MON", "TUE", "WED", "THU", "FRI", "SAT", "SUN"]
        all_days_schedule = []

        for week_day in week_days:
            schedule = LessonFetcher.fetch_schedule(
                group_number, week_day, year, season)
            if schedule:
                all_days_schedule.append(schedule)
            else:
                all_days_schedule.append(None)

        return all_days_schedule

    @staticmethod
    def fetch_tomorrow_schedule(group_number, year, season):
        """Запрос расписания на завтра для группы."""
        # Получаем сегодняшний день и добавляем 1 день для получения завтрашнего
        tomorrow = datetime.today() + timedelta(days=1)

        # Маппинг для API, где понедельник = 'MON', вторник = 'TUE' и т.д.
        days_map = {
            0: 'MON',  # Понедельник
            1: 'TUE',  # Вторник
            2: 'WED',  # Среда
            3: 'THU',  # Четверг
            4: 'FRI',  # Пятница
            5: 'SAT',  # Суббота
            6: 'SUN'  # Воскресенье
        }

        # Получаем день недели завтрашнего дня
        tomorrow_week_day = days_map[tomorrow.weekday()]
        # print(f"Запрос расписания на завтра для дня: {tomorrow_week_day}")

        # Получаем расписание для завтрашнего дня
        return LessonFetcher.fetch_schedule(group_number, tomorrow_week_day, year, season)
