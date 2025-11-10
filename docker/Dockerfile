FROM python:3.11-slim

ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

WORKDIR /app

RUN apt-get update && \
    apt-get install -y --no-install-recommends curl wget tzdata && \
    rm -rf /var/lib/apt/lists/*

COPY ./app/src /app/src
COPY ./requirements.txt /app/requirements.txt

RUN pip install --no-cache-dir -r /app/requirements.txt

RUN mkdir -p /config /logs

EXPOSE 8089

CMD ["python", "-u", "/app/src/main.py"]
