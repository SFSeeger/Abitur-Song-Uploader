FROM node:lts AS node_dependencies

COPY src/theme /app/src/theme
WORKDIR /app/src/theme
RUN npm ci


FROM python:3.13-bullseye
ENV DJANGO_LOG_FILE=/app/log/django/django.log
ENV STATIC_ROOT=/app/static
ENV MEDIA_ROOT=/app/media
ENV ENVIRONMENT=production
EXPOSE 8000

LABEL org.opencontainers.image.source=https://github.com/sfseeger/abitur-song-uploader
LABEL org.opencontainers.image.description="A application to manage everything related to an Abitur, be it collecting songs or creating polls for the students to vote on."
LABEL org.opencontainers.image.licenses=MIT

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

CMD ["./entrypoint.sh"]