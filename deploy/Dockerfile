FROM node:lts AS node_dependencies

COPY src/theme /app/src/theme
WORKDIR /app/src/theme
RUN npm ci


FROM python:3.13-bullseye
ENV DJANGO_LOG_FILE=/app/log/django/django.log
ENV STATIC_ROOT=/app/static
ENV MEDIA_ROOT=/app/media
ENV ENVIRONMENT=production

RUN apt update && apt install -y --no-install-recommends default-libmysqlclient-dev default-mysql-client gettext curl ffmpeg

WORKDIR /app/web

RUN useradd --create-home --shell /bin/bash -u 10001  gunicorn
RUN chown -R gunicorn:gunicorn /app

COPY --chown=gunicorn:gunicorn requirements.txt ./
RUN pip install -r requirements.txt --no-cache-dir

USER gunicorn

# Create neccesary folders
RUN mkdir -p /app/log/gunicorn
RUN mkdir -p /app/log/django

COPY --chown=gunicorn:gunicorn deploy/entrypoint.sh ./


COPY --chown=gunicorn:gunicorn src/ ./
COPY --from=node_dependencies --chown=gunicorn:gunicorn /app/src/theme/node_modules ./theme/node_modules
RUN python3 manage.py collectstatic --noinput --force
RUN python3 manage.py compilemessages


LABEL authors="SFSeeger"

CMD ["./entrypoint.sh"]