FROM python:3.8-alpine

# set work directory
WORKDIR /app

# set environment variables
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1
ENV DEBUG 0

RUN apk add build-base

RUN apk update && apk add gcc libc-dev make git libffi-dev openssl-dev python3-dev libxml2-dev libxslt-dev

# install psycopg2
RUN apk update \
    && apk add --virtual build-deps \
    && apk add postgresql-dev \
    && pip install psycopg2 \
    && apk del build-deps


#RUN pip install --upgrade pip setuptools wheel

# install dependencies
COPY ./requirements.txt .
RUN pip install -r requirements.txt

# copy project
COPY . .

# collect static files
#RUN python manage.py collectstatic --noinput

# add and run as non-root user
RUN adduser -D myuser
USER myuser

# run gunicorn
#CMD gunicorn backend.wsgi:application --bind 0.0.0.0:$PORT
