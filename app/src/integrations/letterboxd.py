import logging
import httpx
from bs4 import BeautifulSoup

log = logging.getLogger("letterboxd")

class LetterboxdClient:
    BASE = "https://letterboxd.com"

    def __init__(self, username: str, password: str):
        self.username = username
        self.password = password  # Not used yet (scrape-only)
        self.client = httpx.AsyncClient(timeout=20)

    async def get_watched(self):
        """Scrape diary entries (no official API)."""
        url = f"{self.BASE}/{self.username}/films/diary/"
        try:
            r = await self.client.get(url)
            r.raise_for_status()
            soup = BeautifulSoup(r.text, "lxml")
            films = []
            for li in soup.select("li.diary-entry-row"):
                slug = li.get("data-film-slug")
                if slug:
                    films.append({"slug": slug})
            return films
        except Exception as e:
            log.exception(f"Letterboxd scrape error: {e}")
            return []
