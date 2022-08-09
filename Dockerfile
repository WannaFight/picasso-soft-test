FROM python:3.10

LABEL Author="Ivan Trushin"

ENV PYTHONBUFFERED 1

RUN mkdir "/app"

WORKDIR /app

COPY . /app

RUN pip install -r requirements.txt