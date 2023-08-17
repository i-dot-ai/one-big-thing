FROM python:3.9

ENV PYTHONUNBUFFERED 1
ENV PYTHONDONTWRITEBYTECODE 1
ENV TZ=UTC

RUN ln -snf /usr/share/zoneinfo/$TZ /etc/localtime && echo $TZ > /etc/timezone

RUN python3 -m pip install -U pip setuptools wheel

COPY ./loadtests/requirements.txt /app/requirements.lock
RUN python3 -m pip install -r /app/requirements.lock --no-cache-dir

COPY ./docker/loadtests/entrypoint.sh /entrypoint.sh
RUN chmod +x /entrypoint.sh

COPY ./loadtests /app

WORKDIR /app/

EXPOSE 8089

ENTRYPOINT ["sh","/entrypoint.sh"]
