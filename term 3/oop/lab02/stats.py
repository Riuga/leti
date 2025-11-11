from collections import Counter, defaultdict
from typing import Dict


class CityBuilding:
    """Class for storing city building data"""

    def __init__(self, city: str, street: str, house: str, floor: int):
        self.city = city
        self.street = street
        self.house = house
        self.floor = floor

    def __eq__(self, other):
        if not isinstance(other, CityBuilding):
            return False
        return (self.city == other.city and
                self.street == other.street and
                self.house == other.house and
                self.floor == other.floor)

    def __hash__(self):
        return hash((self.city, self.street, self.house, self.floor))

    def __str__(self):
        return f"{self.city}, {self.street}, house {self.house}, {self.floor} floors"


class CityStatistics:
    """Class for working with city statistics"""

    def __init__(self):
        self.buildings = []

    def add_building(self, building: CityBuilding):
        self.buildings.append(building)

    def find_duplicates(self) -> Dict[CityBuilding, int]:
        """Finds duplicate records"""
        counter = Counter(self.buildings)
        return {building: count for building, count in counter.items() if count > 1}

    def get_floors_statistics(self) -> Dict[str, Dict[int, int]]:
        """Building floor statistics by city"""
        stats = defaultdict(lambda: defaultdict(int))

        for building in self.buildings:
            stats[building.city][building.floor] += 1

        # Convert to regular dict and ensure all floor levels 1-5 are present
        result = {}
        for city, floor_counts in stats.items():
            city_stats = {}
            for floor_num in range(1, 6):
                city_stats[floor_num] = floor_counts.get(floor_num, 0)
            result[city] = city_stats

        return result
