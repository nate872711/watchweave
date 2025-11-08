# ──────────────────────────────────────────────
#   WatchWeave Dockerfile — root build context
# ──────────────────────────────────────────────
FROM python:3.11-slim

ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

WORKDIR /app

# Install base dependencies
RUN apt-get update && \
    apt-get install -y --no-install-recommends curl wget tzdata && \
    rm -rf /var/lib/apt/lists/*

# Copy source and dependencies from the repo root
COPY ./src /app/src
COPY ./requirements.txt /app/requirements.txt

# Install dependencies
RUN pip install --no-cache-dir -r /app/requirements.txt || \
    pip install --no-cache-dir pyyaml requests python-dotenv rich

# Create directories for config and logs
RUN mkdir -p /config /logs

EXPOSE 8089
ENV TZ=Etc/UTC

# Run app
CMD ["python", "-u", "/app/src/main.py"]
