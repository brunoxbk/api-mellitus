# Pull official base image
FROM python:3.12-slim

# Set working directory
WORKDIR /app

# Set environment variables
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

# Install system dependencies
RUN apt-get update \
    && apt-get install -y gcc python3-dev musl-dev libmagic1 libffi-dev build-essential libpq-dev \
    && rm -rf /var/lib/apt/lists/*

# Copy Poetry files
COPY poetry.lock pyproject.toml /app/

# Install Poetry
RUN pip install poetry

# Install dependencies
RUN poetry install --no-interaction --no-ansi

# Copy the application code
COPY . /app/

# Run migrations, collect static files and start Gunicorn
CMD set -xe; \
    poetry run python manage.py migrate --noinput; \
    poetry run python manage.py collectstatic --noinput --clear; \
    poetry run gunicorn mellitus.wsgi:application --bind 0.0.0.0:8000