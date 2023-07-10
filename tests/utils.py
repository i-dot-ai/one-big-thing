import functools

import httpx
import testino

from one_big_thing import wsgi

TEST_SERVER_URL = "http://one_big_thing-testserver:8010/"


def with_client(func):
    @functools.wraps(func)
    def _inner(*args, **kwargs):
        with httpx.Client(app=wsgi.application, base_url=TEST_SERVER_URL) as client:
            return func(client, *args, **kwargs)

    return _inner


def make_testino_client():
    client = testino.WSGIAgent(wsgi.application, TEST_SERVER_URL)
    return client
