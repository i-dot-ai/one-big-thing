from django.contrib.auth.decorators import user_passes_test
from django.shortcuts import render


def unauthorised_view(request):
    return render(request, "unauthorised.html", {}, status=401)


def login_required(func):
    def _inner(request, *args, **kwargs):
        if request.user.is_authenticated:
            return func(request, *args, **kwargs)
        else:
            return unauthorised_view(request)

    return _inner


enforce_user_completes_details_and_pre_survey = user_passes_test(
    lambda user: (user.completed_personal_details and user.has_completed_pre_survey and user.is_active),
    login_url="/intro-pre-survey/",
    redirect_field_name=None,
)
