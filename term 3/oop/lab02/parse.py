import csv
import xml.etree.ElementTree as ET
from stats import CityBuilding, CityStatistics


class FileParser:
    """Base class for file parsing"""

    @staticmethod
    def parse_file(file_path: str) -> CityStatistics:
        raise NotImplementedError("Method must be implemented in subclass")


class XMLParser(FileParser):
    """XML file parser"""

    @staticmethod
    def parse_file(file_path: str) -> CityStatistics:
        statistics = CityStatistics()
        tree = ET.parse(file_path)
        root = tree.getroot()

        for item_elem in root.findall('item'):
            city = item_elem.get('city')
            street = item_elem.get('street')
            house = item_elem.get('house')
            floor = int(item_elem.get('floor'))

            building = CityBuilding(city, street, house, floor)
            statistics.add_building(building)

        return statistics


class CSVParser(FileParser):
    """CSV file parser"""

    @staticmethod
    def parse_file(file_path: str) -> CityStatistics:
        statistics = CityStatistics()

        with open(file_path, 'r', encoding='utf-8') as file:
            reader = csv.DictReader(file, delimiter=';')

            for row in reader:
                city = row['city'].strip('"')
                street = row['street'].strip('"')
                house = row['house']
                floor = int(row['floor'])

                building = CityBuilding(city, street, house, floor)
                statistics.add_building(building)

        return statistics
