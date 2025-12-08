from datetime import datetime


def get_current_season():
    """
    Определяет текущий сезон на основе системного времени.
    Возвращает 'autumn' для месяцев с сентября по декабрь
    и 'spring' для месяцев с февраля по май.
    """
    month = datetime.now().month

    if 9 <= month <= 12:
        return "autumn"
    elif 2 <= month <= 5:
        return "spring"
    else:
        raise ValueError("Сезон не определен для текущего месяца.")


def get_current_year():
    """
    Определяет текущий год на основе системного времени.
    Возвращает год как целое число.
    """
    return datetime.now().year


def get_current_week_day():
    """
    Определяет текущий день недели и возвращает его в формате 'MON', 'TUE', 'WED', и т.д.
    """
    # Массив сокращений дней недели
    week_days = ["MON", "TUE", "WED", "THU", "FRI", "SAT", "SUN"]

    # Определение текущего дня недели (0 - понедельник, 6 - воскресенье)
    current_day_index = datetime.now().weekday()

    return week_days[current_day_index]
