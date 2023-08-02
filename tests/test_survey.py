from one_big_thing.learning import models
from tests import utils


def test_submit_survey():
    test_email = "test-evaluation-data-entry@example.com"
    authenticated_user = {"email": test_email, "password": "giraffe47"}
    client = utils.make_testino_client()
    utils.register(client, **authenticated_user)
    user = models.User.objects.get(email=test_email)
    complete_survey(client, user)


def complete_survey(client, user):
    first_page = client.get("/questions/pre/")

    second_page = step_survey_page(
        first_page,
        "Do you feel confident to make a decision based on information you are presented with? For example, statistics or customer feedback",
        # noqa: E501
        {
            "confident-in-decisions": "confident",
        },
    )

    third_page = step_survey_page(
        second_page,
        "How would you feel about explaining to someone in your team what a graph is showing?",
        {
            "confidence-explaining-graph": "reluctant",
        },
    )

    fourth_page = step_survey_page(
        third_page,
        "Have you designed a survey to gather responses and make a decision?",
        {
            "have-you-designed-a-survey": "yes-i-could-teach-others",
        },
    )

    fifth_page = step_survey_page(
        fourth_page,
        "Have you ever believed something you read online that turned out not to be true?",
        {
            "believed-something-incorrect-online": "yes",
        },
    )

    sixth_page = step_survey_page(
        fifth_page,
        "Do you use any of the following? Spreadsheets (for example, Excel or Google Sheets)",
        {
            "do-you-use-spreadsheets": "create",
        },
    )

    seventh_page = step_survey_page(
        sixth_page,
        "Do you use any of the following? Dashboard tools (for example, Tableau, PowerBI, Looker or Qlik Sense)",
        {
            "do-you-use-dashboard-tools": "create",
        },
    )

    eighth_page = step_survey_page(
        seventh_page,
        "Do you use any of the following? A coding language to explore data (for example, Python, R, SQL , SPSS or STATA)",
        {
            "do-you-use-coding-language": "create",
        },
    )

    assert eighth_page.has_text("Welcome to your One Big Thing Learning Record")
    assert eighth_page.has_text("Based on your survey results, we recommend you do the following:")

    completed_surveys = models.SurveyResult.objects.filter(user=user, survey_type="pre")
    assert len(completed_surveys) > 0, completed_surveys

    competency_data = completed_surveys.get(page_number=1)
    assert competency_data.data == {"confident-in-decisions": "confident"}, competency_data.data

    question_1_data = completed_surveys.get(page_number=2)
    assert question_1_data.data == {
        "confidence-explaining-graph": "reluctant",
    }, question_1_data.data

    question_2_data = completed_surveys.get(page_number=3)
    assert question_2_data.data == {"have-you-designed-a-survey": "yes-i-could-teach-others"}, question_2_data.data


def step_survey_page(page, title, fields):
    assert page.status_code == 200, page.status_code
    assert page.has_text(title)
    form = page.get_form("""form:not([action])""")

    for field in fields:
        form[field] = fields[field]

    next_page = form.submit().follow()
    return next_page
