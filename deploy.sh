#!/bin/bash
set -e
set -u

git pull origin main

pip install -r /home/gunicorn/Abitur-Song-Uploader/requirements.txt
npm install --prefix /home/gunicorn/Abitur-Song-Uploader/src/theme
