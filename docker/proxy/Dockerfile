FROM python:3.9-buster as web

ENV PYTHONUNBUFFERED 1
ENV PYTHONDONTWRITEBYTECODE 1
ENV TZ=UTC

ARG BASE_URL

ENV BASE_URL=${BASE_URL}

RUN ln -snf /usr/share/zoneinfo/$TZ /etc/localtime && echo $TZ > /etc/timezone

RUN python3 -m pip install -U pip setuptools wheel

COPY ./requirements.lock /app/requirements.lock
RUN python3 -m pip install -r /app/requirements.lock --no-cache-dir

COPY . /app

WORKDIR /app/

RUN \
    DJANGO_SETTINGS_MODULE=one_big_thing.settings_base \
    DJANGO_SECRET_KEY="temp" \
    python manage.py collectstatic --no-input

################

FROM nginx:latest

ENV TZ=UTC

RUN ln -snf /usr/share/zoneinfo/$TZ /etc/localtime && echo $TZ > /etc/timezone

COPY ./docker/proxy/start.sh /start.sh
RUN chmod +x /start.sh

COPY --from=web /app/staticfiles /usr/share/nginx/html/static

EXPOSE 80

COPY ./proxy/nginx.conf.template /etc/nginx/templates/default.conf.template


