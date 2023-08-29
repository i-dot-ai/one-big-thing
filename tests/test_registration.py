import uuid

from one_big_thing.learning import email_handler

from . import utils


class MockUser:
    def __init__(self, email):
        self.last_token_sent_at = None
        self.id = uuid.uuid4()
        self.email = email

    def save(self):
        pass


def test_incorrect_token():
    user = MockUser(email="incorrect-token@example.com")
    url = email_handler._make_token_url(user, "email-register")
    client = utils.make_testino_client()

    page = client.get(url)

    assert page.has_text("Login failed")
