FROM python:3.11-bullseye


RUN apt-get update
RUN apt-get install default-libmysqlclient-dev gettext -y
WORKDIR /app/web
COPY src/ ./src/

WORKDIR /app
ADD ./requirements-dev.txt ./
ADD ./entrypoint.sh ./

RUN pip install -r requirements-dev.txt --no-cache-dir 
EXPOSE 80

ENTRYPOINT [ "bash", "/app/entrypoint.sh" ]
# ENTRYPOINT [ "python3", "manage.py", "runserver", "0.0.0.0:8000"]