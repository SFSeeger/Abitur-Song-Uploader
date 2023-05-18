#!/bin/sh

/app/web/manage.py migrate
/app/web/manage.py collectstatic --no-input
/app/web/manage.py compilemessages

/app/web/manage.py qcluster &

python -Xfrozen_modules=off -m debugpy --listen 0.0.0.0:3000 /app/web/manage.py runserver 0.0.0.0:80
