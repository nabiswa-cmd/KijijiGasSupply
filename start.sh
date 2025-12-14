#!/bin/bash
# Install dependencies
pip install -r requirements.txt

# Apply database migrations
python KIJIJIGAS/kijijiGas/manage.py migrate

# Collect static files (optional, needed for static assets)
python KIJIJIGAS/kijijiGas/manage.py collectstatic --noinput

# Run the Django server
python KIJIJIGAS/kijijiGas/manage.py runserver 0.0.0.0:8000

