import WikipediaAPI
import WikipediaSearch


class WikipediaApp:
    """
    App init class
    """

    def __init__(self):
        self.client_api = WikipediaAPI.WikipediaAPI()
        self.client_search = WikipediaSearch.WikipediaSearch(self.client_api)

    def run(self):
        """
        Runs endless loop for user queries. 
        """
        print("Wikipedia search.")
        while True:
            query = input(
                "\nEnter a search query (type 'exit' to exit): ").strip()
            if query.lower() == 'exit':
                print("Exiting application...")
                self.client_api.close()
                break

            titles = self.client_search.perform_search(query)
            if titles:
                self.client_search.open_article(titles)
