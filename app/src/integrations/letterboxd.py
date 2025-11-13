import requests
import logging
from bs4 import BeautifulSoup
from datetime import datetime
import time

log = logging.getLogger("letterboxd")

LOGIN_URL = "https://letterboxd.com/sign-in/"
DIARY_POST_URL = "https://letterboxd.com/ajax/post-entry"

HEADERS = {
    "User-Agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 "
                  "(KHTML, like Gecko) Chrome/123.0.0.0 Safari/537.36"
}


class LetterboxdClient:
    def __init__(self, username, password, enabled=True):
        self.username = username
        self.password = password
        self.enabled = enabled

        self.session = requests.Session()
        self.session.headers.update(HEADERS)

        if self.enabled:
            self.login()

    def login(self):
        """Logs into Letterboxd using form-based authentication."""
        try:
            log.info("🔐 Logging into Letterboxd…")

            # Load login page to grab the CSRF token
            r = self.session.get(LOGIN_URL, timeout=10)
            soup = BeautifulSoup(r.text, "html.parser")
            token = soup.find("input", {"name": "__csrf"})["value"]

            payload = {
                "__csrf": token,
                "username": self.username,
                "password": self.password,
                "remember": "true",
            }

            r = self.session.post(LOGIN_URL, data=payload, timeout=10)

            if "The details you entered did not match our records" in r.text:
                log.error("❌ Letterboxd login failed — bad username/password")
                self.enabled = False
                return

            if "/sign-out/" not in r.text:
                log.error("❌ Letterboxd login failed — unknown cause")
                self.enabled = False
                return

            log.info("✔ Logged into Letterboxd successfully")

        except Exception as e:
            log.error(f"❌ Letterboxd login error: {e}")
            self.enabled = False

    def post_diary_entry(self, movie_title, watched_at, tmdb_id=None):
        """
        Posts a diary entry to Letterboxd.
        """
        if not self.enabled:
            return False

        date_str = watched_at.strftime("%Y-%m-%d")

        payload = {
            "filmSlug": "",
            "diary-entry-date": date_str,
            "diary-entry-time": "",
            "diary-entry-watchedDate": date_str,
            "diary-entry-tags": "",
            "diary-entry-rewatch": "false",
            "includeFriendsComments": "on",
        }

        # If TMDb ID provided, try to pre-resolve slug
        if tmdb_id:
            payload["tmdbId"] = tmdb_id

        try:
            r = self.session.post(DIARY_POST_URL, data=payload, timeout=10)

            if r.status_code == 429:
                log.warning("⏳ Rate limited by Letterboxd — waiting 10 seconds...")
                time.sleep(10)
                return self.post_diary_entry(movie_title, watched_at, tmdb_id)

            if r.status_code != 200:
                log.error(f"❌ Failed to post diary entry ({r.status_code})")
                return False

            log.info(f"📘 Logged on Letterboxd → {movie_title} ({date_str})")
            return True

        except Exception as e:
            log.error(f"❌ Diary posting error: {e}")
            return False

    def sync_watched(self, items):
        """
        Takes watched items from Plex → posts them to Letterboxd.
        """
        if not self.enabled:
            return

        movies = [i for i in items if i.get("type") == "movie"]

        if not movies:
            log.info("ℹ No movies to sync to Letterboxd")
            return

        log.info(f"📤 Syncing {len(movies)} films → Letterboxd")

        for m in movies:
            title = m["title"]
            watched_at = m["watched_at"]
            tmdb_id = m.get("tmdb_id", None)

            self.post_diary_entry(title, watched_at, tmdb_id=tmdb_id)
