FROM python:3.6-alpine

MAINTAINER "fabriziomiano@gmail.com"

COPY . /app

WORKDIR /app

RUN pip install --upgrade pip && pip install -r requirements.txt

EXPOSE 5000

ENTRYPOINT ["gunicorn", "--bind", "0.0.0.0:5000", "app:app"]
