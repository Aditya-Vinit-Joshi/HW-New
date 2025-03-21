#!/usr/bin/env bash
# exit on error
set -o errexit

# Upgrade pip
python -m pip install --upgrade pip

# Install dependencies
pip install -r requirements.txt

# Create necessary directories
mkdir -p staticfiles mediafiles

# Make migrations
python manage.py makemigrations

# Collect static files
python manage.py collectstatic --no-input

# Run migrations
python manage.py migrate

# Create superuser if needed (will be skipped if user exists)
python manage.py createsuperuser --noinput || true 