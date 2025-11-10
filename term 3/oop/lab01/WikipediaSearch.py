import webbrowser


class WikipediaSearch:
    """
    Searcher
    """

    def __init__(self, client_api):
        self.client_api = client_api

    def perform_search(self, query):
        """
        Performs search queries 
        Returns search results
        """
        search_results = self.client_api.search_articles(query)

        if not search_results:
            print("Results not found.")
            return []

        print(f"\nThere is {len(search_results)} results:")
        for i, title in enumerate(search_results[:10], start=1):
            print(f"{i}. {title}")

        return search_results[:10]

    def open_article(self, titles):
        """
        Opens an article with selected title in a browser.
        """
        while True:
            select = input(
                "\nType page number to open ('back' for a new query): ").strip()
            if select.lower() == 'back':
                return

            if select.isdigit() and 1 <= int(select) <= len(titles):
                selected_title = titles[int(select) - 1]
                article_url = self.client_api.get_article_url(selected_title)

                if article_url:
                    print(f"Opening '{selected_title}'...")
                    webbrowser.open(article_url)
                else:
                    print(
                        f"Page URL not found '{selected_title}'.")
                break
            else:
                print("Incorrect input. Type correct page number or 'back'.")
