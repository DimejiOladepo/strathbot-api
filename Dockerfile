# pull official base image
FROM python:3.9-slim-buster

ENV VIRTUAL_ENV=/opt/venv
RUN python3 -m venv $VIRTUAL_ENV
ENV PATH="$VIRTUAL_ENV/bin:$PATH"

# set work directory
WORKDIR /usr/src/app

RUN apt-get update
RUN apt-get install -y ffmpeg

# install dependencies
RUN pip install --upgrade pip

COPY ./requirements.txt /usr/src/app/requirements.txt
RUN pip3 install -r requirements.txt --no-cache-dir

# copy project
COPY . /usr/src/app/