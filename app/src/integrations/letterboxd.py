import logging
import time
from datetime import datetime

import requests
from bs4 import BeautifulSoup

log = logging.getLogger("letterboxd")

LOGIN_URL = "https://letterboxd.com/sign-in/"
DIARY_POST_URL = "https://letterboxd.com/ajax/post-entry"

DEFAULT_HEADERS = {
    "User-Agent": (
        "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 "
        "(KHTML, like Gecko) Chrome/123.0.0.0 Safari/537.36"
    ),
    "Referer": "https://letterboxd.com/",
}


class LetterboxdClient:
    """
    Very lightweight, unofficial Letterboxd diary sync client.

    ⚠ This uses the same endpoints as the website's own forms.
      It may break if Letterboxd changes their HTML or endpoints.
    """

    def __init__(self, username: str, password: str, enabled: bool = False, dry_run: bool = False):
        self.username = username
        self.password = password
        self.enabled = enabled
        self.dry_run = dry_run

        self.session = requests.Session()
        self.session.headers.update(DEFAULT_HEADERS)

        if self.enabled:
            self._login()

    def _login(self) -> None:
        """Perform form-based login and establish a session."""
        try:
            log.info("🔐 Logging into Letterboxd as %s…", self.username)

            r = self.session.get(LOGIN_URL, timeout=15)
            r.raise_for_status()

            soup = BeautifulSoup(r.text, "html.parser")
            token_input = soup.find("input", {"name": "__csrf"})
            if not token_input or not token_input.get("value"):
                log.error("❌ Could not locate CSRF token on Letterboxd login page.")
                self.enabled = False
                return

            csrf_token = token_input["value"]

            payload = {
                "__csrf": csrf_token,
                "username": self.username,
                "password": self.password,
                "remember": "true",
            }

            r = self.session.post(LOGIN_URL, data=payload, timeout=15)
            r.raise_for_status()

            if "The details you entered did not match our records" in r.text:
                log.error("❌ Letterboxd login failed — invalid username or password.")
                self.enabled = False
                return

            if "/sign-out/" not in r.text:
                # Heuristic: logged-in pages always show sign-out link somewhere
                log.error("❌ Letterboxd login failed — could not confirm logged-in state.")
                self.enabled = False
                return

            log.info("✔ Logged into Letterboxd successfully")

        except Exception as e:
            log.error("❌ Letterboxd login error: %s", e, exc_info=True)
            self.enabled = False

    def _post_diary_entry(self, movie_title: str, watched_at: datetime, tmdb_id=None) -> bool:
        """Post a single diary entry."""
        if not self.enabled:
            return False

        date_str = watched_at.strftime("%Y-%m-%d")

        if self.dry_run:
            log.info("🧪 DRY-RUN Letterboxd: would log %s (%s)", movie_title, date_str)
            return True

        payload = {
            "diary-entry-watchedDate": date_str,
            "diary-entry-date": date_str,
            "diary-entry-time": "",
            "diary-entry-tags": "",
            "diary-entry-rewatch": "false",
            "includeFriendsComments": "on",
        }

        if tmdb_id:
            payload["tmdbId"] = tmdb_id

        try:
            r = self.session.post(DIARY_POST_URL, data=payload, timeout=15)
            if r.status_code == 429:
                log.warning("⏳ Rate-limited by Letterboxd; sleeping 10 seconds and retrying once…")
                time.sleep(10)
                r = self.session.post(DIARY_POST_URL, data=payload, timeout=15)

            if r.status_code != 200:
                log.error("❌ Failed to post diary entry (%s) for %s", r.status_code, movie_title)
                return False

            log.info("📘 Logged on Letterboxd → %s (%s)", movie_title, date_str)
            return True

        except Exception as e:
            log.error("❌ Diary posting error for %s: %s", movie_title, e, exc_info=True)
            return False

    def sync_watched(self, items) -> None:
        """
        Takes a list of watched items from Plex and posts movies as diary entries.

        Expected item shape:
        {
            "title": str,
            "type": "movie" | "episode",
            "watched_at": datetime,
            "tmdb_id": Optional[int],
            ...
        }
        """
        if not self.enabled:
            log.info("Letterboxd disabled — skipping Letterboxd sync.")
            return

        movies = [i for i in items if i.get("type") == "movie"]

        if not movies:
            log.info("ℹ No movies to sync to Letterboxd.")
            return

        log.info("📤 Syncing %d films → Letterboxd (dry_run=%s)", len(movies), self.dry_run)

        for m in movies:
            title = m.get("title", "Unknown title")
            watched_at = m.get("watched_at")
            tmdb_id = m.get("tmdb_id")

            if not isinstance(watched_at, datetime):
                # fallback if we ever get strings
                try:
                    watched_at = datetime.fromisoformat(str(watched_at))
                except Exception:
                    watched_at = datetime.utcnow()

            self._post_diary_entry(title, watched_at, tmdb_id=tmdb_id)
