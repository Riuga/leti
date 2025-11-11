import xml.etree.ElementTree as ET
import time
import os
from typing import Tuple
from parse import CSVParser, XMLParser
from stats import CityStatistics


class CityStatisticsApp:
    """Main application class"""

    def __init__(self):
        self.parsers = {
            '.xml': XMLParser(),
            '.csv': CSVParser()
        }

    def get_file_extension(self, file_path: str) -> str:
        """Returns file extension"""
        return os.path.splitext(file_path)[1].lower()

    def is_supported_format(self, file_path: str) -> bool:
        """Checks if file format is supported"""
        extension = self.get_file_extension(file_path)
        return extension in self.parsers and os.path.exists(file_path)

    def parse_city_file(self, file_path: str) -> Tuple[CityStatistics, float]:
        """Parses file and returns statistics and processing time"""
        start_time = time.time()

        extension = self.get_file_extension(file_path)
        parser = self.parsers[extension]
        statistics = parser.parse_file(file_path)

        processing_time = time.time() - start_time
        return statistics, processing_time

    def display_statistics(self, statistics: CityStatistics, processing_time: float):
        """Displays statistics"""
        print("\n" + "="*60)
        print("FILE PROCESSING STATISTICS")
        print("="*60)

        # 1. Duplicate records
        duplicates = statistics.find_duplicates()
        if duplicates:
            print("\n1. DUPLICATE RECORDS:")
            for building, count in duplicates.items():
                print(f"   {building}")
                print(f"   Repetitions: {count}\n")
        else:
            print("\n1. Duplicate records: not found")

        # 2. Building floor statistics
        floors_stats = statistics.get_floors_statistics()
        print("\n2. BUILDING FLOOR STATISTICS BY CITY:")
        for city_name, city_floors in floors_stats.items():
            print(f"   {city_name}:")
            total_buildings = sum(city_floors.values())
            for floor_num in range(1, 6):
                count = city_floors.get(floor_num, 0)
                percentage = (count / total_buildings *
                              100) if total_buildings > 0 else 0
                print(
                    f"     {floor_num}-floor buildings: {count} ({percentage:.1f}%)")
            print(f"     Total buildings: {total_buildings}\n")

        # 3. Processing time
        print(f"\n3. FILE PROCESSING TIME: {processing_time:.3f} seconds")
        print("="*60)

    def run(self):
        """Main application loop"""
        print("CITY BUILDING DIRECTORY ANALYSIS APPLICATION")
        print("Supported formats: .xml, .csv")
        print("Enter 'exit' or 'quit' to exit")

        while True:
            try:
                user_input = input("\nEnter path to directory file: ").strip()

                if user_input.lower() in ('exit', 'quit'):
                    print("Shutting down application...")
                    break

                if not user_input:
                    print("Error: path cannot be empty")
                    continue

                if not self.is_supported_format(user_input):
                    print("Error: file does not exist or format is not supported")
                    print("Supported formats: .xml, .csv")
                    continue

                try:
                    statistics, processing_time = self.parse_city_file(
                        user_input)
                    self.display_statistics(statistics, processing_time)

                except Exception as e:
                    print(f"Error processing file: {e}")
                    print("Make sure the file has correct structure")

            except KeyboardInterrupt:
                print("\n\nShutting down application...")
                break
            except Exception as e:
                print(f"Unexpected error: {e}")
