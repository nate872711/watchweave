# ──────────────────────────────────────────────
#   WatchWeave Dockerfile
#   Python 3.11-slim base image
#   Fixes import errors and YAML dependency
# ──────────────────────────────────────────────

FROM python:3.11-slim

# Prevent Python from writing .pyc files and buffering stdout
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

# ──────────────────────────────────────────────
#   Set up working directory
#   /app is the root; /app/src holds the code
# ──────────────────────────────────────────────
WORKDIR /app

# ──────────────────────────────────────────────
#   Install system dependencies
# ──────────────────────────────────────────────
RUN apt-get update && \
    apt-get install -y --no-install-recommends \
        curl \
        wget \
        tzdata \
    && rm -rf /var/lib/apt/lists/*

# ──────────────────────────────────────────────
#   Copy project files
# ──────────────────────────────────────────────
COPY src/ /app/src/
COPY requirements.txt /app/

# ──────────────────────────────────────────────
#   Install Python dependencies
# ──────────────────────────────────────────────
# PyYAML is explicitly installed for config generation
RUN pip install --no-cache-dir -r requirements.txt || \
    pip install --no-cache-dir pyyaml requests python-dotenv rich

# ──────────────────────────────────────────────
#   Create config and log directories
# ──────────────────────────────────────────────
RUN mkdir -p /config /logs

# ──────────────────────────────────────────────
#   Expose default internal port
# ──────────────────────────────────────────────
EXPOSE 8089

# ──────────────────────────────────────────────
#   Environment variables (overridable)
# ──────────────────────────────────────────────
ENV TZ=Etc/UTC

# ──────────────────────────────────────────────
#   Default command — runs main entry point
# ──────────────────────────────────────────────
CMD ["python", "-u", "/app/src/main.py"]
