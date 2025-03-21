#!/usr/bin/env bash
# exit on error
set -o errexit

# Upgrade pip and install build dependencies
python -m pip install --upgrade pip
pip install wheel setuptools

# Install Python dependencies
pip install -r requirements.txt

# Create static and media directories if they don't exist
mkdir -p staticfiles mediafiles

# Collect static files
python manage.py collectstatic --no-input

# Run database migrations
python manage.py migrate

# Create cache table
python manage.py createcachetable

# Check for any obvious issues
python manage.py check --deploy 