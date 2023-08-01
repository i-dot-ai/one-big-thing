from tests import utils
from one_big_thing.learning import models

LOGIN_REQUIRED_PAGES = [
    "/",
    "/home/",
    "/record-learning/",
    "/questions/pre/",
    "/questions/post/",
    "/complete-hours/",
    "/send-learning-record/",
    "/download-learning/",
    "/test/",
]


@utils.with_authenticated_client
def test_get_pages_logged_in(client):
    for url in LOGIN_REQUIRED_PAGES:
        response = client.get(url)
        assert response.status_code == 200


@utils.with_client
def test_get_pages_require_login(client):
    for url in LOGIN_REQUIRED_PAGES:
        response = client.get(url)
        assert response.status_code == 302
