#!/bin/sh

./web/manage.py migrate
./web/manage.py collectstatic --no-input
./web/manage.py compilemessages

./web/manage.py qcluster &

python -Xfrozen_modules=off -m debugpy --wait-for-client --listen 0.0.0.0:3000 ./web/manage.py runserver 0.0.0.0:80
