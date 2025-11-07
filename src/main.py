#!/usr/bin/env python3
"""
WatchWeave — Unified Media Sync Service
---------------------------------------
Synchronizes watched history, lists, and ratings between Plex, Trakt,
Letterboxd, IMDb, and Tautulli.
"""

import os
import time
import yaml
import logging
import requests
from datetime import datetime

CONFIG_PATH = "/config/config.yml"


# =====================================================
# CONFIG MANAGEMENT
# =====================================================

def generate_config_from_env():
    """Generate /config/config.yml from environment variables if missing."""
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
    """Load existing config or generate new one if missing."""
    if not os.path.exists(CONFIG_PATH):
        generate_config_from_env()
    with open(CONFIG_PATH, "r") as f:
        return yaml.safe_load(f)


def save_config(config):
    """Save config back to file (used when refreshing tokens)."""
    with open(CONFIG_PATH, "w") as f:
        yaml.dump(config, f, sort_keys=False)


# =====================================================
# TRAKT TOKEN REFRESH
# =====================================================

def refresh_trakt_token(config):
    """Automatically refresh Trakt access token if available."""
    trakt = config.get("trakt", {})
    if not trakt.get("enabled") or not trakt.get("refresh_token"):
        return config

    logging.info("🔄 Checking Trakt token validity...")

    try:
        res = requests.post(
            "https://api.trakt.tv/oauth/token",
            json={
                "refresh_token": trakt["refresh_token"],
                "client_id": trakt["client_id"],
                "client_secret": trakt["client_secret"],
                "redirect_uri": "urn:ietf:wg:oauth:2.0:oob",
                "grant_type": "refresh_token",
            },
            timeout=10,
        )

        if res.status_code == 200:
            data = res.json()
            trakt["access_token"] = data["access_token"]
            trakt["refresh_token"] = data.get("refresh_token", trakt["refresh_token"])
            trakt["last_refreshed"] = datetime.utcnow().isoformat()
            save_config(config)
            logging.info("✅ Trakt token refreshed successfully.")
        else:
            logging.warning(f"⚠️ Trakt token refresh failed ({res.status_code}): {res.text}")
    except Exception as e:
        logging.error(f"❌ Error refreshing Trakt token: {e}")

    return config


# =====================================================
# TAUTULLI API INTEGRATION
# =====================================================

def get_tautulli_activity(config):
    """Fetch current activity and recent history from Tautulli."""
    tautulli = config.get("tautulli", {})
    if not tautulli.get("enabled"):
        return None

    api_url = tautulli.get("api_url")
    api_key = tautulli.get("api_key")

    if not api_url or not api_key:
        logging.warning("⚠️ Tautulli enabled but missing API credentials.")
        return None

    logging.info("📊 Fetching Tautulli activity...")

    try:
        res = requests.get(
            f"{api_url}?apikey={api_key}&cmd=get_activity",
            timeout=10,
        )
        res.raise_for_status()
        activity = res.json().get("response", {}).get("data", {})
        streams = activity.get("sessions", [])
        logging.info(f"🎞️ Active streams: {len(streams)}")
        return streams
    except Exception as e:
        logging.error(f"❌ Error fetching Tautulli activity: {e}")
        return None


def get_tautulli_history(config, length=20):
    """Fetch recent playback history from Tautulli."""
    tautulli = config.get("tautulli", {})
    if not tautulli.get("enabled"):
        return []

    api_url = tautulli.get("api_url")
    api_key = tautulli.get("api_key")

    try:
        res = requests.get(
            f"{api_url}?apikey={api_key}&cmd=get_history&length={length}",
            timeout=10,
        )
        res.raise_for_status()
        data = res.json().get("response", {}).get("data", {}).get("data", [])
        logging.info(f"📚 Retrieved {len(data)} Tautulli history entries.")
        return data
    except Exception as e:
        logging.error(f"❌ Error fetching Tautulli history: {e}")
        return []


# =====================================================
# SYNC PLACEHOLDERS
# =====================================================

def sync_plex_to_trakt(config, tautulli_history):
    logging.info("🔁 Syncing Plex → Trakt (placeholder)...")
    # TODO: Use tautulli_history to confirm Plex watches before syncing
    if tautulli_history:
        logging.info(f"ℹ️ Using {len(tautulli_history)} entries from Tautulli for validation.")
    time.sleep(1)


def sync_trakt_to_letterboxd(config):
    logging.info("🔁 Syncing Trakt → Letterboxd (placeholder)...")
    time.sleep(1)


def sync_imdb_to_trakt(config):
    logging.info("🔁 Syncing IMDb → Trakt (placeholder)...")
    time.sleep(1)


# =====================================================
# MAIN LOOP
# =====================================================

def main():
    config = load_config()

    logging.basicConfig(
        level=config["server"].get("log_level", "INFO"),
        format="[%(asctime)s] [%(levelname)s] %(message)s",
        datefmt="%Y-%m-%d %H:%M:%S",
    )

    logging.info("🚀 WatchWeave starting up...")
    logging.info(f"🕒 Sync interval: {config['sync']['interval_minutes']} minutes")

    config = refresh_trakt_token(config)

    while True:
        try:
            logging.info("🔄 Beginning sync cycle...")

            # Fetch Tautulli data before sync
            tautulli_history = get_tautulli_history(config)
            get_tautulli_activity(config)

            # Run syncs
            if config["plex"]["enabled"] and config["trakt"]["enabled"]:
                sync_plex_to_trakt(config, tautulli_history)

            if config["trakt"]["enabled"] and config["letterboxd"]["enabled"]:
                sync_trakt_to_letterboxd(config)

            if config["imdb"]["enabled"] and config["trakt"]["enabled"]:
                sync_imdb_to_trakt(config)

            logging.info("✅ Sync cycle complete. Sleeping...")
            time.sleep(config["sync"]["interval_minutes"] * 60)

        except KeyboardInterrupt:
            logging.info("🛑 WatchWeave stopped manually.")
            break
        except Exception as e:
            logging.error(f"❌ Error during sync cycle: {e}")
            time.sleep(30)


if __name__ == "__main__":
    main()
