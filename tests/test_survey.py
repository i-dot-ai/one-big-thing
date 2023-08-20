from one_big_thing.learning import models
from tests import utils


def test_submit_survey():
    test_email = "test-evaluation-data-entry@example.com"
    authenticated_user = {"email": test_email, "password": "GIRAFFE47!x"}
    client = utils.make_testino_client()
    utils.register(client, **authenticated_user)
    user = models.User.objects.get(email=test_email)
    utils.complete_survey(client, user)
    user.delete()


def test_homepage_assigns_awareness():
    test_email = "test-awareness@example.com"
    authenticated_user = {"email": test_email, "password": "GIRAFFE47!x"}
    client = utils.make_testino_client()
    utils.register(client, **authenticated_user)
    user = models.User.objects.get(email=test_email)
    comptency_answers = ["not-confident", "not-confident", "confident"]
    utils.complete_survey(client, user, competency_level_answers=comptency_answers)
    homepage = client.get("/home/")
    assert homepage.has_text("your level is: Awareness")
    user.delete()


def test_homepage_assigns_working():
    test_email = "test-working@example.com"
    authenticated_user = {"email": test_email, "password": "GIRAFFE47!x"}
    client = utils.make_testino_client()
    utils.register(client, **authenticated_user)
    user = models.User.objects.get(email=test_email)
    comptency_answers = ["confident", "not-confident", "confident"]
    utils.complete_survey(client, user, competency_level_answers=comptency_answers)
    homepage = client.get("/home/")
    assert homepage.has_text("your level is: Working")
    user.delete()


def test_homepage_assigns_practitioner():
    test_email = "test-practitioner@example.com"
    authenticated_user = {"email": test_email, "password": "GIRAFFE47!x"}
    client = utils.make_testino_client()
    utils.register(client, **authenticated_user)
    user = models.User.objects.get(email=test_email)
    comptency_answers = ["confident", "very-confident", "very-confident"]
    utils.complete_survey(client, user, competency_level_answers=comptency_answers)
    homepage = client.get("/home/")
    assert homepage.has_text("your level is: Practitioner")
    user.delete()
