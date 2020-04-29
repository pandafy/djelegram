FROM python:3.8-slim-buster

MAINTAINER PANDAFY

ENV PYTHONUNBUFFERED 1

COPY ./requirements.txt /requirements.txt

RUN pip install -U pip wheel setuptools
RUN apt update
RUN apt install gcc -y 
RUN pip install -r requirements.txt

RUN mkdir /app
WORKDIR /app
COPY ./  /app
RUN apt install curl -y 
RUN adduser --disabled-login user
USER user

EXPOSE 8000

