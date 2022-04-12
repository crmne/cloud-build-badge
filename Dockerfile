# syntax=docker/dockerfile:1.3

FROM python:3.9-alpine

RUN mkdir /app
WORKDIR /app

ADD requirements.txt .
RUN pip install -r requirements.txt

ADD main.py .

ENTRYPOINT [/app/badge.py]
