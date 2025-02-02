FROM python:3.11-bullseye

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

ENV NODE_VERSION=16.13.0


RUN apt-get update
RUN apt-get install -y default-libmysqlclient-dev default-mysql-client gettext curl ffmpeg

RUN curl -o- https://raw.githubusercontent.com/nvm-sh/nvm/v0.39.0/install.sh | bash
ENV NVM_DIR=/root/.nvm
RUN . "$NVM_DIR/nvm.sh" && nvm install ${NODE_VERSION}
RUN . "$NVM_DIR/nvm.sh" && nvm use v${NODE_VERSION}
RUN . "$NVM_DIR/nvm.sh" && nvm alias default v${NODE_VERSION}
ENV PATH="/root/.nvm/versions/node/v${NODE_VERSION}/bin/:${PATH}"

WORKDIR /app/web
COPY --chown=root:root src/ ./src/

WORKDIR /app/web/theme
COPY --chown=root:root src/theme/ .
RUN npm i
WORKDIR /app
ADD ./requirements-dev.txt ./
ADD ./entrypoint.sh ./

RUN pip install -r requirements-dev.txt --no-cache-dir 
EXPOSE 80
EXPOSE 3000

WORKDIR /app/web
ENTRYPOINT [ "bash", "/app/entrypoint.sh" ]