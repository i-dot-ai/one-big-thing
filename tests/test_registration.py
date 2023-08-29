import uuid

from one_big_thing.learning import email_handler, models

from . import utils


class MockUser:
    def __init__(self, email):
        self.last_token_sent_at = None
        self.last_login = None
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


def test_reused_token():
    email = "double-login@example.com"
    user = models.User.objects.create_user(email=email)
    assert not user.last_login
    url = email_handler._make_token_url(user, "email-register")
    client = utils.make_testino_client()

    page = client.get(url).follow().follow()

    assert page.has_text("Thank you for signing in to your One Big Thing account")
    user = models.User.objects.get(email=email)
    assert user.last_login

    page = client.get(url)

    assert page.has_text("Login failed")
