from typing import List, Optional


class Lesson:
    def __init__(self,
                 teacher: Optional[str] = None,
                 second_teacher: Optional[str] = None,
                 subject_type: Optional[str] = None,
                 week: Optional[str] = None,
                 name: Optional[str] = None,
                 start_time: Optional[str] = None,
                 end_time: Optional[str] = None,
                 start_time_seconds: Optional[int] = None,
                 end_time_seconds: Optional[int] = None,
                 room: Optional[str] = None,
                 comment: Optional[str] = None,
                 form: Optional[str] = None,
                 temp_changes: Optional[List[str]] = None,
                 url: Optional[str] = None):
        self.teacher = teacher
        self.second_teacher = second_teacher
        self.subject_type = subject_type
        self.week = week
        self.name = name
        self.start_time = start_time
        self.end_time = end_time
        self.start_time_seconds = start_time_seconds
        self.end_time_seconds = end_time_seconds
        self.room = room
        self.comment = comment
        self.form = form
        self.temp_changes = temp_changes if temp_changes is not None else []
        self.url = url

    # Геттеры и сеттеры
    def get_teacher(self) -> Optional[str]:
        return self.teacher

    def set_teacher(self, teacher: str):
        self.teacher = teacher

    def get_second_teacher(self) -> Optional[str]:
        return self.second_teacher

    def set_second_teacher(self, second_teacher: str):
        self.second_teacher = second_teacher

    def get_subject_type(self) -> Optional[str]:
        return self.subject_type

    def set_subject_type(self, subject_type: str):
        self.subject_type = subject_type

    def get_week(self) -> Optional[str]:
        return self.week

    def set_week(self, week: str):
        self.week = week

    def get_name(self) -> Optional[str]:
        return self.name

    def set_name(self, name: str):
        self.name = name

    def get_start_time(self) -> Optional[str]:
        return self.start_time

    def set_start_time(self, start_time: str):
        self.start_time = start_time

    def get_end_time(self) -> Optional[str]:
        return self.end_time

    def set_end_time(self, end_time: str):
        self.end_time = end_time

    def get_start_time_seconds(self) -> Optional[int]:
        return self.start_time_seconds

    def set_start_time_seconds(self, start_time_seconds: int):
        self.start_time_seconds = start_time_seconds

    def get_end_time_seconds(self) -> Optional[int]:
        return self.end_time_seconds

    def set_end_time_seconds(self, end_time_seconds: int):
        self.end_time_seconds = end_time_seconds

    def get_room(self) -> Optional[str]:
        return self.room

    def set_room(self, room: str):
        self.room = room

    def get_comment(self) -> Optional[str]:
        return self.comment

    def set_comment(self, comment: str):
        self.comment = comment

    def get_form(self) -> Optional[str]:
        return self.form

    def set_form(self, form: str):
        self.form = form

    def get_temp_changes(self) -> List[str]:
        return self.temp_changes

    def set_temp_changes(self, temp_changes: List[str]):
        self.temp_changes = temp_changes

    def get_url(self) -> Optional[str]:
        return self.url

    def set_url(self, url: str):
        self.url = url

    def __repr__(self):
        return (
            f"Lesson(name='{self.name}', teacher='{self.teacher}', "
            f"second_teacher='{self.second_teacher}', subject_type='{self.subject_type}', "
            f"week='{self.week}', start_time='{self.start_time}', "
            f"end_time='{self.end_time}', room='{self.room}', url='{self.url}')"
        )
