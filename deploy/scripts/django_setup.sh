#!/bin/bash
python3 ./src/manage.py migrate
python3 ./src/manage.py collectstatic --no-input
python3 ./src/manage.py compilemessages

python3 ./src/manage.py qcluster &

gunicorn -c ./src/config/gunicorn/dev.py
