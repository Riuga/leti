from parser.get_data import RequestCreator
from parser.lesson import Lesson


class Day:
    def __init__(self, name, lessons=None):
        self.name = name
        self.lessons = lessons if lessons is not None else []

    def __repr__(self):
        lessons_str = "\n".join([repr(lesson) for lesson in self.lessons])
        return f"Day(name='{self.name}', lessons=[\n{lessons_str}\n])"

    @classmethod
    def from_api(cls, url: str):
        request_creator = RequestCreator()
        result = request_creator.search_result(url)

        if not result:
            print("Ошибка: Пустой ответ от API.")
            return []

        print("Полный ответ API:", result)

        group_key = "3351"
        if group_key not in result:
            print(f"Ключ '{group_key}' отсутствует в ответе.")
            return []

        group_data = result[group_key]
        days = []
        if "days" in group_data:
            for day_key, day_data in group_data["days"].items():
                lessons = [
                    Lesson(
                        name=lesson.get("name", "Без названия"),
                        teacher=lesson.get("teacher", "Без преподавателя"),
                        subject_type=lesson.get("subjectType", ""),
                        start_time=lesson.get("start_time", ""),
                        end_time=lesson.get("end_time", ""),
                        room=lesson.get("room", "Без аудитории"),
                    )
                    for lesson in day_data.get("lessons", [])
                ]
                day = cls(day_data.get("name", "Без названия дня"), lessons)
                days.append(day)
        else:
            print("Ключ 'days' отсутствует в данных группы.")

        return days
