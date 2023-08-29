from django.contrib.auth.decorators import user_passes_test
from django.shortcuts import render


def unauthorised_view(request):
    return render(request, "unauthorised.html", {}, status=401)


enforce_user_completes_pre_survey = user_passes_test(
    lambda user: (user.has_completed_pre_survey and user.is_active),
    login_url="/intro-pre-survey/",
    redirect_field_name=None,
)
