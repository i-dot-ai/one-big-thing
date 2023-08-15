FROM python:3.9

ENV PYTHONUNBUFFERED 1
ENV PYTHONDONTWRITEBYTECODE 1
ENV TZ=UTC

ARG BASE_URL

ENV BASE_URL=${BASE_URL}

RUN ln -snf /usr/share/zoneinfo/$TZ /etc/localtime && echo $TZ > /etc/timezone

RUN curl -o /bin/wait-for-db https://github.com/palfrey/wait-for-db/releases/download/v1.2.0/wait-for-db-linux-x86
RUN chmod +x /bin/wait-for-db

RUN python3 -m pip install -U pip setuptools wheel

COPY ./requirements.lock /app/requirements.lock
RUN python3 -m pip install -r /app/requirements.lock --no-cache-dir

COPY ./docker/web/start.sh /start.sh
RUN chmod +x /start.sh

COPY ./docker/web/entrypoint.sh /entrypoint.sh
RUN chmod +x /entrypoint.sh

COPY . /app

WORKDIR /app/

RUN \
    DJANGO_SETTINGS_MODULE=one_big_thing.settings_base \
    DJANGO_SECRET_KEY="temp" \
    python manage.py collectstatic --no-input

EXPOSE 8012

ENTRYPOINT ["sh","/entrypoint.sh"]
CMD ["sh","/start.sh"]