<p align="center">
<img src="/branding/plexboxd-banner.png" width="300">


# 🍿 Plexboxd
**Your Plex movies, your Letterboxd diary — finally in sync.**

Plexboxd is a lightweight Flask webhook service that listens to **Tautulli playback events** and logs completed Plex watches as **Letterboxd diary entries (CSV)**.



## Features
- Auto-logs completed **movies** from Tautulli webhooks
- Converts 1–10 ratings to Letterboxd’s 0.5–5★ scale
- Dedupes recent plays and detects rewatches
- Docker-ready and configurable via `.env`

## Future Improvements
- Trakt Syncing
- imdb Syncing
- Collections, Lists & Watchlists Syncing

## Quick start (Docker)
```bash
cp .env.example .env
docker compose -f docker/docker-compose.yml up -d --build
```
### Example docker compose
```yaml
services:
  plexboxd:
    container_name: plexboxd
    image: nate8727/plexboxd:latest
    build:
      context: ..
      dockerfile: docker/Dockerfile
    restart: unless-stopped
    environment:
      # Core configuration
      - TZ=UTC
      - PLEX_BASE_URL=${PLEX_BASE_URL}
      - PLEX_TOKEN=${PLEX_TOKEN}

      # Letterboxd CSV sync
      - CSV_PATH=${CSV_PATH:-/config/letterboxd_diary.csv}
      - DEDUPE_DAYS=${DEDUPE_DAYS:-2}
      - MIN_PERCENT=${MIN_PERCENT:-85}

      # Trakt integration
      - TRAKT_CLIENT_ID=${TRAKT_CLIENT_ID}
      - TRAKT_CLIENT_SECRET=${TRAKT_CLIENT_SECRET}
      - TRAKT_ACCESS_TOKEN=${TRAKT_ACCESS_TOKEN}
      - TRAKT_REDIRECT_URI=${TRAKT_REDIRECT_URI}
      - ENABLE_TRAKT_SYNC=${ENABLE_TRAKT_SYNC:-true}

      # IMDb integration
      - IMDB_RATINGS_CSV=${IMDB_RATINGS_CSV:-/config/imdb/ratings.csv}
      - IMDB_WATCHLIST_CSV=${IMDB_WATCHLIST_CSV:-/config/imdb/watchlist.csv}
      - ENABLE_WATCHLIST_SYNC=${ENABLE_WATCHLIST_SYNC:-true}
      - ENABLE_COLLECTION_SYNC=${ENABLE_COLLECTION_SYNC:-true}

      # Optional webhook notifications
      - WEBHOOK_URL=${WEBHOOK_URL:-}

    volumes:
      - ./data:/config
    ports:
      - "8089:8089"
    command: >
      bash -c "
        echo 'Starting Plexboxd sync service...';
        python -m src.main
      "
```

Service will listen on `http://0.0.0.0:${PORT}/webhook/tautulli` (default `8089`).

## Tautulli setup
- **Notifier:** Webhook
- **URL:** `http://YOUR_SERVER:8089/webhook/tautulli`
- **Header (optional):** `X-Webhook-Secret: <WEBHOOK_SECRET>`
- **Trigger:** Playback Stopped
- **Payload (JSON example):**
```json
{
  "event": "{event}",
  "media_type": "{media_type}",
  "title": "{title}",
  "year": "{year}",
  "imdb_id": "{imdb_id}",
  "tmdb_id": "{themoviedb_id}",
  "user": "{username}",
  "user_rating": "{user_rating}",
  "percent_complete": "{percent_complete}",
  "stopped": "{stopped}"
}
```

## Local dev
```bash
python3 -m venv .venv && source .venv/bin/activate
pip install -r requirements.txt
export FLASK_ENV=development
python -m src.main
```

## Output
CSV written to `${CSV_PATH}` (default `/data/letterboxd_diary_queue.csv`). Import at **Letterboxd → Settings → Import Diary**.

## License
MIT © 2025 nate872711
