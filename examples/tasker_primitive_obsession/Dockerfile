FROM python:3.9-slim

ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1
ENV POETRY_VIRTUALENVS_CREATE=false
ENV POETRY_NO_INTERACTION=1

WORKDIR /app

RUN apt-get update && apt-get install -y \
    gcc \
    libpq-dev \
    && rm -rf /var/lib/apt/lists/*

RUN pip install --no-cache-dir "poetry==1.7.1"

COPY . .

RUN poetry install --with dev --no-interaction

ENV PYTHONPATH=/app/src

ENTRYPOINT ["examples/tasker_primitive_obsession/docker-entrypoint.sh"]
