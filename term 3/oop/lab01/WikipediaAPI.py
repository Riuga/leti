import requests

# Wikipedia API const
WIKIPEDIA_API_URL = "https://ru.wikipedia.org/w/api.php"


class WikipediaAPI:
    """
    Interacting with the Wikipedia API.
    """

    def __init__(self, api_url=WIKIPEDIA_API_URL):
        self.api_url = api_url
        self.session = requests.Session()
        # Headers for browser imitation
        self.session.headers.update({
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36',
            'Accept': 'application/json',
            'Accept-Language': 'ru-RU,ru;q=0.9,en-US;q=0.8,en;q=0.7',
        })

    def search_articles(self, query):
        """
        Returns titles list 
        """
        params = {
            "action": "query",
            "list": "search",
            "srsearch": query,
            "format": "json",
            "utf8": 1,
            "srlimit": 10
        }

        try:
            response = self.session.get(
                self.api_url, params=params, timeout=10)
            response.raise_for_status()
            data = response.json()

            search_results = data.get("query", {}).get("search", [])
            return [result['title'] for result in search_results]
        except requests.RequestException as e:
            print(f"Request error: {e}")
            return []

    def get_article_url(self, title):
        """
        Returns an URL of selected article 
        """
        params = {
            "action": "query",
            "prop": "info",
            "inprop": "url",
            "titles": title,
            "format": "json",
            "utf8": 1,
        }

        try:
            response = self.session.get(
                self.api_url, params=params, timeout=10)
            response.raise_for_status()
            data = response.json()

            pages = data.get("query", {}).get("pages", {})
            for page_id, page_data in pages.items():
                if page_id != "-1":
                    return page_data.get("fullurl")
            return None
        except requests.RequestException as e:
            print(f"Request error: {e}")
            return None

    def close(self):
        """Closing session"""
        print("Closing session...")
        self.session.close()
