#!/bin/bash
/app/web/manage.py migrate
/app/web/manage.py createcachetable

gunicorn \
    --log-level info \
    --capture-output \
    --access-logfile /app/log/gunicorn/access.log \
    --error-logfile /app/log/gunicorn/error.log \
    --workers 4 \
    --timeout 120 \
    --bind 0.0.0.0:8000 \
    songuploader.wsgi:application