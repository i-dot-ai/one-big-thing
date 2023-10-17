from one_big_thing.learning import models

from . import utils


def test_step_through_change_details():
    email = "hi@example.com"
    client = utils.make_testino_client()
    utils.register(client, email=email, password=None, pre_survey=True)
    page = client.get("/my-details/")
    form = page.get_form()
    form["grade"] = "HIGHER_EXECUTIVE_OFFICER"
    form["profession"] = "COMMERCIAL"
    page.has_text("Submit")
    page = form.submit().follow()
    assert page.has_text("One Big Thing overview")  # homepage
    user = models.User.objects.get(email=email)
    assert user.grade == "HIGHER_EXECUTIVE_OFFICER", user.grade
    assert user.profession == "COMMERCIAL", user.profession
    assert user.new_department.code == "cabinet-office", user.new_department.code
    user.delete()


def test_validation_about_you():
    client = utils.make_testino_client()
    # Register/login
    page = client.get("/")
    form = page.get_form()
    form["email"] = "email@example.com"
    form.submit().follow()
    url = utils._get_latest_email_url()
    client.get(url)
    # Now test "about you"
    page = client.get("/").follow().follow().follow()
    assert page.has_text("About you")
    form = page.get_form()
    form["profession"] = "DIGITAL_DATA_AND_TECHNOLOGY"
    page = form.submit()
    assert page.has_text("About you")
    assert page.has_text("Next")
    assert page.has_text("There is a problem")
    models.User.objects.get(email="email@example.com").delete()


def test_my_details_redirect():
    """
    Does it redirect even when user has completed pre-survey but not
    completed details?
    """
    email = "no_details@example.com"
    user = models.User(email=email, has_completed_pre_survey=True)
    user.save()
    client = utils.make_testino_client()
    # Login
    page = client.get("/")
    form = page.get_form()
    form["email"] = email
    form.submit().follow()
    url = utils._get_latest_email_url()
    client.get(url)
    # Check pages redirect
    page = client.get("/").follow().follow().follow()
    assert page.has_text("About you")
    page = client.get("/record-learning/").follow().follow()
    assert page.has_text("About you")
    page = client.get("/home/").follow().follow()
    assert page.has_text("About you")
    page = client.get("/intro-pre-survey/").follow()
    assert page.has_text("About you")
