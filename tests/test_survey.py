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


# def complete_survey(client, user, competency_level_answers=["confident", "not-confident", "not-confident"]):
#     first_page = client.get("/questions/pre/")

#     second_page = step_survey_page(
#         first_page,
#         "How would you feel about making a decision based on information you're presented with? This might be numerical data like statistics or non-numerical data like user feedback.",  # noqa: E501
#         # noqa: E501
#         {
#             "confident-in-decisions": competency_level_answers[0],
#         },
#     )

#     third_page = step_survey_page(
#         second_page,
#         "How would you feel about designing a graphic to communicate the results of a survey? This could be an infographic, chart or other visualisation.",
#         {
#             "confidence-graphic-survey": competency_level_answers[1],
#         },
#     )

#     fourth_page = step_survey_page(
#         third_page,
#         "How would you feel about explaining to someone in your team what a chart of performance data is showing?",
#         {
#             "confidence-explaining-chart": competency_level_answers[2],
#         },
#     )

#     fifth_page = step_survey_page(
#         fourth_page,
#         "To what extent do you agree or disagree with the following statement?",
#         {
#             "aware-of-the-aims": 1,
#         },
#     )

#     sixth_page = step_survey_page(
#         fifth_page,
#         "To what extent do you agree or disagree with the following statements?",
#         {
#             "shared-identity": 2,
#             "identity-is-important": 1,
#         },
#     )

#     seventh_page = step_survey_page(
#         sixth_page,
#         "To what extent do you agree or disagree with the following statements?",
#         {
#             "confident-day-to-day": 1,
#             "data-is-relevant-to-role": 1,
#             "use-data-effectively-day-to-day": 5,
#             "data-support-day-to-day": 1,
#         },
#     )
#     eighth_page = step_survey_page(
#         seventh_page,
#         "Are you currently a line manager?",
#         {
#             "line-manager": "yes",
#         },
#     )
#     ninth_page = step_survey_page(
#         eighth_page,
#         'If you answered "yes" to the previous question, to what extent do you agree or disagree with the following statements?',
#         {"help-team": "yes", "support-team": "dont-know", "coach-team": "no"},
#     )
#     tenth_page = step_survey_page(
#         ninth_page,
#         "In the last 6 months, have you done any type of training?",
#         {
#             "training-last-six-months": "yes",
#         },
#     )
#     completed_page = step_survey_page(
#         tenth_page,
#         'If you answered "yes" to the previous question, did it have an analytical component (eg data, evaluation)',
#         {
#             "training-analytical-component": "yes",
#         },
#     )

#     assert completed_page.has_text("Survey completed")
#     assert completed_page.has_text("You can now start your One Big Thing learning.")

#     completed_surveys = models.SurveyResult.objects.filter(user=user, survey_type="pre")
#     assert len(completed_surveys) > 0, completed_surveys

#     competency_data = completed_surveys.get(page_number=1)
#     assert competency_data.data == {"confident-in-decisions": "confident"}, competency_data.data

#     question_data = completed_surveys.get(page_number=2)
#     assert question_data.data == {
#         "confidence-graphic-survey": "not-confident",
#     }, question_data

#     question_data = completed_surveys.get(page_number=3)
#     assert question_data.data == {"confidence-explaining-chart": "not-confident"}, question_data.data


# def step_survey_page(page, title, fields):
#     assert page.status_code == 200, page.status_code
#     assert page.has_text(title), title
#     form = page.get_form("""form:not([action])""")

#     for field in fields:
#         form[field] = fields[field]

#     next_page = form.submit().follow()
#     return next_page


# TODO - check assignment of levels

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