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

## Quick start (Docker)
```bash
cp .env.example .env
docker compose -f docker/docker-compose.yml up -d --build
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
