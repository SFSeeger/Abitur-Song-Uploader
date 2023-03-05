#!/bin/sh

./web/manage.py migrate
./web/manage.py collectstatic --no-input
./web/manage.py compilemessages

./web/manage.py qcluster &

./web/manage.py runserver 0.0.0.0:80
