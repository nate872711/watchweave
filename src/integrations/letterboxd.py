import logging
def get_letterboxd_watchlist(config):
    l = config.get("letterboxd",{})
    if not l.get("enabled"): return []
    logging.info("Letterboxd list fetch (placeholder)"); return []
