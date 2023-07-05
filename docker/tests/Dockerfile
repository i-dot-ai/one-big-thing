FROM python:3.8-buster

ENV PYTHONUNBUFFERED 1
ENV PYTHONDONTWRITEBYTECODE 1
ENV TZ=UTC

RUN ln -snf /usr/share/zoneinfo/$TZ /etc/localtime && echo $TZ > /etc/timezone

RUN apt update -y && apt install -y postgresql-client

RUN curl -o /bin/wait-for-db https://github.com/palfrey/wait-for-db/releases/download/v1.2.0/wait-for-db-linux-x86
RUN chmod +x /bin/wait-for-db

RUN python3 -m pip install -U pip setuptools wheel

COPY ./requirements-dev.lock /app/requirements-dev.lock
RUN python3 -m pip install -r /app/requirements-dev.lock --no-cache-dir

COPY ./docker/tests/entrypoint.sh /entrypoint.sh
RUN chmod +x /entrypoint.sh

COPY ./docker/tests/start.sh /start.sh
RUN chmod +x /start.sh

COPY . /app

WORKDIR /app/

RUN \
    DJANGO_SETTINGS_MODULE=one_big_thing.settings_base \
    DJANGO_SECRET_KEY="temp" \
    python manage.py collectstatic --no-input

ENTRYPOINT ["sh","/entrypoint.sh"]
CMD ["sh","/start.sh"]
