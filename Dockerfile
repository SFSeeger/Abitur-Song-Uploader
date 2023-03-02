FROM python:3.11-bullseye

WORKDIR /app

COPY src .
COPY requirements-dev.txt requirements-dev.txt
COPY entrypoint.sh entrypoint.sh

RUN apt-get update
RUN apt-get install default-libmysqlclient-dev -y

RUN pip install -r requirements-dev.txt --no-cache-dir 
EXPOSE 80

ENTRYPOINT [ "./manage.py", "runserver", "0.0.0.0:80" ]