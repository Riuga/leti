import WikipediaApp

"""
Entry point
"""
if __name__ == "__main__":
    try:
        app = WikipediaApp.WikipediaApp()
        app.run()
    except KeyboardInterrupt:
        print("\nExiting...")
