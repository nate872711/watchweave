import os
import yaml
import logging

CONFIG_PATH = "/config/config.yml"


def generate_config_from_env():
    """Generate /config/config.yml from environment variables if it doesn't exist."""
    os.makedirs("/config", exist_ok=True)

    config = {
        "server": {
            "timezone": os.getenv("TZ", "UTC"),
            "log_level": os.getenv("LOG_LEVEL", "INFO"),
        },
        "plex": {
            "enabled": os.getenv("PLEX_ENABLED", "false").lower() == "true",
            "server_url": os.getenv("PLEX_SERVER_URL"),
            "token": os.getenv("PLEX_TOKEN"),
            "username": os.getenv("PLEX_USERNAME"),
        },
        "tautulli": {
            "enabled": os.getenv("TAUTULLI_ENABLED", "false").lower() == "true",
            "api_url": os.getenv("TAUTULLI_API_URL"),
            "api_key": os.getenv("TAUTULLI_API_KEY"),
        },
        "letterboxd": {
            "enabled": os.getenv("LETTERBOXD_ENABLED", "false").lower() == "true",
            "username": os.getenv("LETTERBOXD_USERNAME"),
            "password": os.getenv("LETTERBOXD_PASSWORD"),
        },
        "trakt": {
            "enabled": os.getenv("TRAKT_ENABLED", "false").lower() == "true",
            "client_id": os.getenv("TRAKT_CLIENT_ID"),
            "client_secret": os.getenv("TRAKT_CLIENT_SECRET"),
            "access_token": os.getenv("TRAKT_ACCESS_TOKEN"),
            "refresh_token": os.getenv("TRAKT_REFRESH_TOKEN"),
        },
        "imdb": {
            "enabled": os.getenv("IMDB_ENABLED", "false").lower() == "true",
            "import_csv_path": os.getenv("IMDB_CSV_PATH"),
        },
        "sync": {
            "interval_minutes": int(os.getenv("SYNC_INTERVAL_MINUTES", "30")),
            "direction": os.getenv("SYNC_DIRECTION", "plex->trakt,letterboxd,imdb"),
        },
    }

    with open(CONFIG_PATH, "w") as f:
        yaml.dump(config, f, sort_keys=False)

    logging.info("✅ Config generated from environment variables.")


def load_config():
    """Load existing config or generate a new one if missing."""
    if not os.path.exists(CONFIG_PATH):
        generate_config_from_env()
    with open(CONFIG_PATH, "r") as f:
        return yaml.safe_load(f)
