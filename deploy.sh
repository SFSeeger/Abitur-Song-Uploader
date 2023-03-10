#!/bin/bash
set -e
set -u

source /home/gunicorn/.venv/bin/activate

pip install -r /home/gunicorn/Abitur-Song-Uploader/requirements.txt
npm install --prefix /home/gunicorn/Abitur-Song-Uploader/src/theme
