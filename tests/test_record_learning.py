import httpx
from nose import with_setup

from one_big_thing import wsgi
from one_big_thing.learning import models
from tests import utils


def setup_user_and_learning_record():
    user, _ = models.User.objects.get_or_create(email="peter.rabbit@example.com")
    user.set_password("P455W0rd")
    user.save()
    models.Learning(user=user, title="Learning about data 1", link="http://example.com", time_to_complete=60).save()
    models.Learning(user=user, title="Learning about data 2", link="http://example.com", time_to_complete=120).save()
    models.Learning(user=user, title="Learning about data 3", link="http://example.com", time_to_complete=240).save()
    models.Course(title="Course 1", time_to_complete=60).save()


def teardown_user_and_learning_record():
    user = models.User.objects.get(email="peter.rabbit@example.com")
    user.delete()
    models.Course.objects.filter(title="Course 1").delete()


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


@utils.with_authenticated_client
def test_download_learning_document(client):
    response = client.get("/download-learning/")
    assert response.status_code == 200, response.status_code
    assert (
        response.headers["Content-Type"] == "application/vnd.openxmlformats-officedocument.wordprocessingml.document"
    ), response["Content-Type"]


@with_setup(setup_user_and_learning_record, teardown_user_and_learning_record)
def test_delete_learning():
    user_email = "peter.rabbit@example.com"
    learning_to_delete = models.Learning.objects.get(user__email=user_email, title="Learning about data 1")
    with httpx.Client(app=wsgi.application, base_url=utils.TEST_SERVER_URL, follow_redirects=True) as client:
        response = client.get("/accounts/login/")
        csrf = response.cookies["csrftoken"]
        data = {"login": user_email, "password": "P455W0rd"}
        headers = {"X-CSRFToken": csrf}
        response = client.post("/accounts/login/", data=data, headers=headers)
        csrf = response.cookies["csrftoken"]
        headers = {"X-CSRFToken": csrf}
        response = client.post(f"remove-learning/{learning_to_delete.pk}/", headers=headers)
        assert response.status_code == 200, response.status_code
        learning_for_user_qs = models.Learning.objects.filter(user__email="peter.rabbit@example.com")
        assert learning_for_user_qs.count() == 2, learning_for_user_qs.count()
        titles = learning_for_user_qs.values_list("title", flat=True)
        assert "Learning about data 1" not in titles, titles
