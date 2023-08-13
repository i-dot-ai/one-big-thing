from one_big_thing.learning import models
from tests import utils


def test_enter_invalid_time_to_complete():
    test_email = "test-learning-record-invalid-time-entry@example.com"
    authenticated_user = {"email": test_email, "password": "!$giraFFe47"}
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
    assert submitted_page.has_text("Please enter the minutes this course took to complete, between 1 and 59")

    user.delete()


def test_enter_invalid_values():
    test_email = "test-learning-record-invalid-data-entry@example.com"
    authenticated_user = {"email": test_email, "password": "$%gIraffe47"}
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
    assert submitted_page.has_text("Please enter the minutes this course took to complete, between 1 and 59")
    assert submitted_page.has_text("Please provide a title for this course")

    user.delete()


def test_enter_valid_learning_record():
    test_email = "test-learning-record-valid-data-entry@example.com"
    authenticated_user = {"email": test_email, "password": "&&GIraffe47$"}
    client = utils.make_testino_client()
    utils.register(client, **authenticated_user)
    user = models.User.objects.get(email=test_email)

    record_learning_page = client.get("/record-learning/")
    assert record_learning_page.status_code == 200, record_learning_page.status_code
    assert record_learning_page.has_text("Record learning I've done:")

    record_learning_form = record_learning_page.get_form()
    record_learning_form["title"] = "Test correct course"
    record_learning_form["time_to_complete_minutes"] = 0
    record_learning_form["time_to_complete_hours"] = 2
    record_learning_form["link"] = "https://google.co.uk"
    record_learning_form["learning_type"] = "OTHER"

    submitted_page = record_learning_form.submit().follow()
    assert submitted_page.status_code == 200, submitted_page.status_code
    assert submitted_page.has_text("Test correct course")
    assert submitted_page.has_text("2 hours")
    assert submitted_page.has_text("Other")

    user.delete()


def test_completed_learning_record_feedback_link():
    test_email = "test123@example.com"
    authenticated_user = {"email": test_email, "password": "P455W0rd!£"}
    client = utils.make_testino_client()
    utils.register(client, **authenticated_user)
    user = models.User.objects.get(email=test_email)

    record_learning_page = client.get("/record-learning/")
    assert record_learning_page.status_code == 200
    assert record_learning_page.has_text("Record learning I've done:")

    record_learning_form = record_learning_page.get_form()
    record_learning_form["title"] = "Test full day course"
    record_learning_form["time_to_complete_minutes"] = 0
    record_learning_form["time_to_complete_hours"] = 10
    record_learning_form["link"] = "https://example.com"
    record_learning_form["learning_type"] = "VIDEO"

    submitted_page = record_learning_form.submit().follow()
    assert submitted_page.status_code == 200, submitted_page.status_code
    assert submitted_page.has_text("Test full day course")
    assert submitted_page.has_text("10 hours")
    assert submitted_page.has_text("Video or documentary")
    assert submitted_page.has_text("You should provide feedback about your One Big Thing experience.")

    user.delete()


def test_enter_learning_record_streamlined():
    test_email = "test@example.com"
    authenticated_user = {"email": test_email, "password": "Giraffe@@47"}
    client = utils.make_testino_client()
    utils.register(client, **authenticated_user)
    user = models.User.objects.get(email=test_email)
    user.department = "home-office"
    user.save()

    record_learning_page = client.get("/record-learning/")
    assert record_learning_page.status_code == 200
    assert record_learning_page.has_text("Record learning I've done")

    record_learning_form = record_learning_page.get_form()
    record_learning_form["time_to_complete_minutes"] = 15
    record_learning_form["time_to_complete_hours"] = 2
    submitted_page = record_learning_form.submit().follow()
    assert submitted_page.status_code == 200, submitted_page.status_code
    assert submitted_page.has_text("Completed department content")
    assert submitted_page.has_text("2 hours and 15 minutes")
    assert not submitted_page.has_text("You should provide feedback about your One Big Thing experience.")

    record_learning_form = record_learning_page.get_form()
    record_learning_form["time_to_complete_minutes"] = 0
    record_learning_form["time_to_complete_hours"] = 7
    submitted_page = record_learning_form.submit().follow()
    assert submitted_page.has_text("You should provide feedback about your One Big Thing experience.")
    assert submitted_page.has_text("9 hours and 15 minutes")
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
    authenticated_user = {"email": user_email, "password": "Giraffe%$47"}
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
    record_page = client.get("/record-learning/")
    assert record_page.has_text("Learning about data 1")
    assert record_page.has_text("Learning about data 2")
    assert record_page.has_text("Learning about data 3")
    learning_to_delete = models.Learning.objects.get(user__email=user_email, title="Learning about data 1")
    delete_page = client.get(f"/delete-learning-check/{learning_to_delete.id}/")
    record_page = delete_page.get_form().submit(extra={"cancel": ""}).follow()
    assert record_page.has_text("Learning about data 1")
    delete_page = client.get(f"/delete-learning-check/{learning_to_delete.id}/")
    delete_form = delete_page.get_form()
    record_page = delete_form.submit(extra={"delete-learning": ""}).follow()
    assert not record_page.has_text("Learning about data 1")
    assert record_page.has_text("Learning about data 2")
    assert record_page.has_text("Learning about data 3")


def test_create_delete_learning_streamlined():
    user_email = "test-delete-learning-record-streamlined@example.com"
    authenticated_user = {"email": user_email, "password": "Giraffe47!!"}
    client = utils.make_testino_client()
    utils.register(client, **authenticated_user)
    user = models.User.objects.get(email=user_email)
    user.department = "home-office"
    user.save()
    record_page = client.get("/record-learning/")
    record_learning_form = record_page.get_form()
    record_learning_form["time_to_complete_minutes"] = 4
    record_learning_form["time_to_complete_hours"] = 2
    submitted_page = record_learning_form.submit().follow()
    assert submitted_page.status_code == 200, submitted_page.status_code
    assert submitted_page.has_text("Completed department content")
    assert submitted_page.has_text("2 hours and 4 minutes")
    dept_learning = models.Learning.objects.filter(user__email=user_email).last()
    delete_page = client.get(f"/delete-learning-check/{dept_learning.id}/")
    delete_form = delete_page.get_form()
    record_page = delete_form.submit(extra={"delete-learning": ""}).follow()
    assert not record_page.has_text("Completed department content")
    assert not record_page.has_text("2 hours and 4 minutes")
