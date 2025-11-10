FROM python:3.11-slim

ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

WORKDIR /app

# OS dependencies
RUN apt-get update && \
    apt-get install -y --no-install-recommends curl wget tzdata && \
    rm -rf /var/lib/apt/lists/*

# Copy entire app folder
COPY ./app/src /app/src
COPY ./requirements.txt /app/requirements.txt

# Install dependencies
RUN pip install --no-cache-dir -r /app/requirements.txt || \
    pip install --no-cache-dir pyyaml requests python-dotenv rich

# Create config + logs folders
RUN mkdir -p /config /logs

EXPOSE 8089

CMD ["python", "-u", "/app/src/main.py"]
