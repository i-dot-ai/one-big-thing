from one_big_thing.learning import models
from tests import utils


def test_enter_invalid_time_to_complete():
    test_email = "test-learning-record-invalid-time-entry@example.com"
    authenticated_user = {"email": test_email, "password": "giraffe47"}
    client = utils.make_testino_client()
    utils.register(client, **authenticated_user)
    user = models.User.objects.get(email=test_email)

    record_learning_page = client.get("/record-learning/")
    assert record_learning_page.status_code == 200
    assert record_learning_page.has_text("Record learning I've done:")

    record_learning_form = record_learning_page.get_form()
    record_learning_form["title"] = "Test incorrect time"
    record_learning_form["time_to_complete_minutes"] = "e"
    record_learning_form["time_to_complete_hours"] = "e"

    submitted_page = record_learning_form.submit()
    assert submitted_page.status_code == 200, submitted_page.status_code
    assert submitted_page.has_text("Please enter the hours this course took to complete e.g. 2")
    assert submitted_page.has_text("Please enter the minutes this course took to complete e.g. 45")

    user.delete()


def test_enter_invalid_values():
    test_email = "test-learning-record-invalid-data-entry@example.com"
    authenticated_user = {"email": test_email, "password": "giraffe47"}
    client = utils.make_testino_client()
    utils.register(client, **authenticated_user)
    user = models.User.objects.get(email=test_email)

    record_learning_page = client.get("/record-learning/")
    assert record_learning_page.status_code == 200
    assert record_learning_page.has_text("Record learning I've done:")

    record_learning_form = record_learning_page.get_form()

    submitted_page = record_learning_form.submit()
    assert submitted_page.status_code == 200, submitted_page.status_code
    assert submitted_page.has_text("Please enter the hours this course took to complete e.g. 2")
    assert submitted_page.has_text("Please enter the minutes this course took to complete e.g. 45")
    assert submitted_page.has_text("Please provide a title for this course")

    user.delete()


def test_enter_valid_learning_record():
    test_email = "test-learning-record-valid-data-entry@example.com"
    authenticated_user = {"email": test_email, "password": "giraffe47"}
    client = utils.make_testino_client()
    utils.register(client, **authenticated_user)
    user = models.User.objects.get(email=test_email)

    record_learning_page = client.get("/record-learning/")
    assert record_learning_page.status_code == 200
    assert record_learning_page.has_text("Record learning I've done:")

    record_learning_form = record_learning_page.get_form()
    record_learning_form["title"] = "Test correct course"
    record_learning_form["time_to_complete_minutes"] = 0
    record_learning_form["time_to_complete_hours"] = 2
    record_learning_form["link"] = "https://google.co.uk"
    record_learning_form["learning_type"] = "LINK"

    submitted_page = record_learning_form.submit().follow()
    assert submitted_page.status_code == 200, submitted_page.status_code
    assert submitted_page.has_text("Test correct course")
    assert submitted_page.has_text("2 hours")
    assert submitted_page.has_text("Link")

    user.delete()
