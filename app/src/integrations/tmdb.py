import tmdbsimple as tmdb
from rich import print


class TMDbClient:
    def __init__(self, api_key: str):
        tmdb.API_KEY = api_key
        self.api = tmdb

        print("[green]TMDb client ready")

    def search_movie(self, query):
        search = self.api.Search()
        response = search.movie(query=query)
        return response.get("results", [])
