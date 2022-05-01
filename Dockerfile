FROM python:3.8.2


WORKDIR /app

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

RUN apt-get update \
    && apt-get -y install libpq-dev gcc

EXPOSE 8000


COPY . .
RUN pip install -U pip
RUN python3 -m pip install -r req.txt

