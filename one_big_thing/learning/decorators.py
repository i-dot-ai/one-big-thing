from django.contrib.auth.decorators import user_passes_test

enforce_user_completes_pre_survey = user_passes_test(
    lambda user: (user.has_completed_pre_survey and user.is_active),
    login_url="/intro-pre-survey/",
    redirect_field_name=None,
)
