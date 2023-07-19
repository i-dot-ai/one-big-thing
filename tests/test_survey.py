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
        "Question 1",
        {
            "sentient": 3,
        },
    )

    completed_page = step_survey_page(
        third_page,
        "Question 2",
        {
            "big": 1,
            "wide": 5,
        },
    )

    assert completed_page.has_text("Survey completed!")

    completed_surveys = models.SurveyResult.objects.filter(user=user, survey_type="pre")
    assert len(completed_surveys) > 0, completed_surveys

    competency_data = completed_surveys.get(page_number=1)
    assert competency_data.data == {"competency": "beginner"}, competency_data.data

    question_1_data = completed_surveys.get(page_number=2)
    assert question_1_data.data == {"sentient": "3"}, question_1_data.data

    question_2_data = completed_surveys.get(page_number=3)
    assert question_2_data.data == {"big": "1", "wide": "5"}, question_2_data.data


def step_survey_page(page, title, fields):
    assert page.status_code == 200, page.status_code
    assert page.has_text(title)
    form = page.get_form("""form:not([action])""")

    for field in fields:
        form[field] = fields[field]

    next_page = form.submit().follow()
    return next_page