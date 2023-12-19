import pytest


@pytest.mark.parametrize(
    "survey_type, page_number, payload, expected_has_completed_pre_survey, expected_has_completed_post_survey, expected_redirect",  # noqa
    [
        ("pre", 1, {"confident-in-decisions": "very-confident"}, False, False, "/questions/pre/2/"),
        ("pre", 9, {"shared-identity": "1", "identity-is-important": "2"}, True, False, "/end-pre-survey/"),
        (
            "awareness",
            1,
            {
                "i-understand-what-data-means": "1",
                "better-at-interpreting-data": "2",
                "interested-in-working-with-data-in-day-to-day": "3",
                "more-confident-using-data-for-decisions": "4",
                "more-confident-communicating-data-to-influence-decisions": "4",
            },
            False,
            False,
            "/questions/awareness/2/",
        ),
        ("awareness", 8, {"willing-to-follow-up": "yes"}, False, True, "/end-post-survey/"),
        ("post", 1, {"training-level": "yes"}, False, False, "/questions/post/2/"),
        ("post", 5, {"willing-to-follow-up": "yes"}, False, True, "/home/"),
    ],
)
@pytest.mark.django_db
def test_questions_view(
    create_user,
    client,
    survey_type,
    page_number,
    payload,
    expected_has_completed_pre_survey,
    expected_has_completed_post_survey,
    expected_redirect,
):
    user = create_user(email="someone@example.com")
    client.force_login(user)
    url = f"/questions/{survey_type}/{page_number}/"
    response = client.post(url, data=payload)

    user.refresh_from_db()
    assert user.has_completed_pre_survey == expected_has_completed_pre_survey
    assert user.has_completed_post_survey == expected_has_completed_post_survey
    assert response.status_code == 302
    assert response.url == expected_redirect
