import logging
from . import plex, trakt, letterboxd, imdb
from .utils import extract_imdb_id_from_guid
def run_sync_cycle(config) -> dict:
    summary = {"plex->trakt_updated": 0, "plex_count": 0, "trakt_count": 0, "imdb_ratings": 0, "letterboxd_items": 0}
    direction = (config.get("sync", {}).get("direction") or "").lower()
    plex_watched = plex.get_plex_watched(config)
    trakt_watched = trakt.get_trakt_watched(config)
    imdb_ratings = imdb.get_imdb_ratings(config.get("imdb", {}).get("import_csv_path"))
    lboxd = letterboxd.get_letterboxd_watchlist(config)
    summary["plex_count"] = len(plex_watched); summary["trakt_count"] = len(trakt_watched); summary["imdb_ratings"] = len(imdb_ratings); summary["letterboxd_items"] = len(lboxd)
    trakt_imdb_ids = {m["ids"]["imdb"] for m in trakt_watched if m.get("ids", {}).get("imdb")}
    if "plex->trakt" in direction or "bidirectional" in direction:
        for p in plex_watched:
            imdb_id = p.get("imdb") or extract_imdb_id_from_guid(p.get("guid","") if "guid" in p else "")
            if imdb_id and imdb_id not in trakt_imdb_ids:
                if trakt.mark_trakt_watched_imdb(config, imdb_id): summary["plex->trakt_updated"] += 1
    if "trakt->plex" in direction or "bidirectional" in direction: logging.info("Trakt->Plex watched sync placeholder.")
    if lboxd: logging.info("Letterboxd items available: %s", len(lboxd))
    if imdb_ratings: logging.info("IMDb ratings available: %s", len(imdb_ratings))
    logging.info("Cycle complete. Plex->Trakt updates=%s", summary["plex->trakt_updated"])
    return summary
