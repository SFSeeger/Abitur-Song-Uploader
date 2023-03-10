#!/bin/bash
set -e
set -u

source /home/gunicorn/.venv/bin/activate

python3 /home/gunicorn/Abitur-Song-Uploader/src/manage.py migrate
python3 /home/gunicorn/Abitur-Song-Uploader/src/manage.py collectstatic --no-input
python3 /home/gunicorn/Abitur-Song-Uploader/src/manage.py compilemessages

python3 /home/gunicorn/Abitur-Song-Uploader/src/manage.py qcluster &

gunicorn -c /home/gunicorn/Abitur-Song-Uploader/src/config/gunicorn/dev.py
