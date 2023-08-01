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


@utils.with_authenticated_client
def test_download_learning_document(client):
    response = client.get("/download-learning/")
    assert response.status_code == 200, response.status_code
    assert (
        response.headers["Content-Type"] == "application/vnd.openxmlformats-officedocument.wordprocessingml.document"
    ), response["Content-Type"]


def test_delete_learning():
    user_email = "test-delete-learning-record@example.com"
    authenticated_user = {"email": user_email, "password": "giraffe47"}
    client = utils.make_testino_client()
    utils.register(client, **authenticated_user)
    user = models.User.objects.get(email=user_email)
    models.Learning(
        user=user,
        title="Learning about data 1",
        link="http://example.com",
        time_to_complete=60,
    ).save()
    models.Learning(
        user=user,
        title="Learning about data 2",
        link="http://example.com",
        time_to_complete=120,
    ).save()
    models.Learning(
        user=user,
        title="Learning about data 3",
        link="http://example.com",
        time_to_complete=240,
    ).save()
    models.Course(title="Course 1", time_to_complete=60).save()
    learning_to_delete = models.Learning.objects.get(user__email=user_email, title="Learning about data 1")
    page = client.get("/record-learning/")
    assert page.has_text("Learning about data 1")
    assert page.has_text("Learning about data 2")
    assert page.has_text("Learning about data 3")
    form = page.get_form(f"""form[action="/remove-learning/{learning_to_delete.id}/"]""")
    page = form.submit().follow()
    assert not page.has_text("Learning about data 1")
    assert page.has_text("Learning about data 2")
    assert page.has_text("Learning about data 3")
