import logging, requests
from .utils import extract_imdb_id_from_guid
def _headers(token): return {"X-Plex-Token": token} if token else {}
def get_plex_watched(config):
    plex = config.get("plex",{})
    if not plex.get("enabled"): return []
    token, server = plex.get("token"), plex.get("server_url")
    if not token or not server: logging.warning("Plex missing config"); return []
    try:
        url = f"{server}/library/all?type=1&viewCount%3E=1"
        r = requests.get(url, headers=_headers(token), timeout=15); items = []
        try: items = r.json().get("MediaContainer",{}).get("Metadata",[])
        except Exception: items = []
        movies = []
        for i in items:
            imdb = extract_imdb_id_from_guid(i.get("guid",""))
            movies.append({"title": i.get("title"), "year": i.get("year"), "imdb": imdb, "ratingKey": i.get("ratingKey")})
        logging.info("Plex watched parsed: %s", len(movies))
        return movies
    except Exception as e:
        logging.warning("Plex fetch error: %s", e); return []
