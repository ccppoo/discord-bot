FROM python:3.8-slim

# install git for installing dependencies via pip <repository>
RUN apt-get update && \
    apt-get upgrade -y && \
    apt-get install -y git

# add user (change to whatever you want)
# prevents running sudo commands
RUN useradd -r -s /bin/bash alex

# set current env
ENV HOME /app
WORKDIR /app
ENV PATH="/app/.local/bin:${PATH}"

RUN chown -R alex:alex /app
USER alex

# set argument vars in docker-run command
ARG AWS_ACCESS_KEY_ID
ARG AWS_SECRET_ACCESS_KEY
ARG AWS_DEFAULT_REGION

# ENV AWS agrument
ENV AWS_ACCESS_KEY_ID $AWS_ACCESS_KEY_ID
ENV AWS_SECRET_ACCESS_KEY $AWS_SECRET_ACCESS_KEY
ENV AWS_DEFAULT_REGION $AWS_DEFAULT_REGION

# set Discord APP token argument
ARG DISCORD_BOT_TOKEN

# ENV discord argument
ENV DISCORD_BOT_TOKEN $DISCORD_BOT_TOKEN

# DISTINGUISH DEVELOPMENT <-> DISTRIBUTE / true == 1, false == 0
ENV RELEASE $RELEASE

# Avoid cache purge by adding requirements first
ADD ./requirements.txt ./requirements.txt

RUN pip install --upgrade pip --user
RUN pip install --no-cache-dir -r ./requirements.txt --user

# Add the rest of the files
COPY . /app
WORKDIR /app

# start discord bot
CMD ["python", "app.py"]
