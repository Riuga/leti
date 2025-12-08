import requests


class RequestCreator:
    """Класс для выполнения запросов к API."""

    def search_result(self, url: str) -> dict:
        headers = {
            'Authorization': 'Bearer YOUR_TOKEN',  # Замените на ваш токен
            'Content-Type': 'application/json'
        }
        try:
            print(f"Запрос к API: {url}")
            response = requests.get(url, headers=headers)
            print(f"Код ответа: {response.status_code}")

            if response.status_code == 200:
                return response.json()
            else:
                print(f"Ошибка: Код ответа {response.status_code}")
                return {}
        except Exception as e:
            print(f"Ошибка при выполнении запроса: {e}")
            return {}
