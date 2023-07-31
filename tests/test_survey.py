from one_big_thing.learning import models
from tests import utils


def test_submit_survey():
    test_email = "test-evaluation-data-entry@example.com"
    authenticated_user = {"email": test_email, "password": "giraffe47"}
    client = utils.make_testino_client()
    utils.register(client, **authenticated_user)
    user = models.User.objects.get(email=test_email)

    competency_page = client.get("/questions/pre/")

    second_page = step_survey_page(
        competency_page,
        "Competency",
        {
            "competency": "beginner",
        },
    )

    third_page = step_survey_page(
        second_page,
        "Create a unifying experience and build a shared identity (or create a shared vision, define shared goals)",
        {
            "aims": 3,
            "shared-identity": 3,
            "identity-is-important": 3,
        },
    )

    completed_page = step_survey_page(
        third_page,
        "Uplift in data awareness",
        {
            "positive-day-to-day": 1,
            "effective-day-to-day": 5,
        },
    )

    assert completed_page.has_text("Welcome to your One Big Thing Learning Record")
    assert completed_page.has_text("Based on your survey results, we recommend you do the following:")

    completed_surveys = models.SurveyResult.objects.filter(user=user, survey_type="pre")
    assert len(completed_surveys) > 0, completed_surveys

    competency_data = completed_surveys.get(page_number=1)
    assert competency_data.data == {"competency": "beginner"}, competency_data.data

    question_1_data = completed_surveys.get(page_number=2)
    assert question_1_data.data == {
        "aims": "3",
        "shared-identity": "3",
        "identity-is-important": "3",
    }, question_1_data.data

    question_2_data = completed_surveys.get(page_number=3)
    assert question_2_data.data == {"positive-day-to-day": "1", "effective-day-to-day": "5"}, question_2_data.data


def step_survey_page(page, title, fields):
    assert page.status_code == 200, page.status_code
    assert page.has_text(title)
    form = page.get_form("""form:not([action])""")

    for field in fields:
        form[field] = fields[field]

    next_page = form.submit().follow()
    return next_page
