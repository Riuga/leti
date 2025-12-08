from typing import Dict
from parser.day import Day


class GroupData:
    def __init__(self, group: str = None, days: Dict[str, Day] = None):
        self.group = group
        self.days = days if days is not None else {}

    def get_group(self) -> str:
        return self.group

    def set_group(self, group: str):
        self.group = group

    def get_days(self) -> Dict[str, Day]:
        return self.days

    def set_days(self, days: Dict[str, Day]):
        self.days = days

    def __repr__(self) -> str:
        return f"GroupData(group='{self.group}', days={self.days})"
