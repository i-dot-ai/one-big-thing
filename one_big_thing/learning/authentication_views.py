import logging

from django.contrib import messages
from django.contrib.auth import login, logout
from django.core.exceptions import ValidationError
from django.core.validators import validate_email
from django.shortcuts import redirect, render
from django.urls import reverse
from django.views.decorators.http import require_http_methods

from one_big_thing.learning import email_handler, models, restrict_email
from one_big_thing.learning.utils import MethodDispatcher

logger = logging.getLogger(__name__)


def _strip_microseconds(dt):
    if not dt:
        return None
    return dt.replace(microsecond=0, tzinfo=None)


@require_http_methods(["GET", "POST"])
class CustomLoginView(MethodDispatcher):
    template_name = "login.html"
    error_message = "Something has gone wrong.  Please try again."

    def error(self, request):
        messages.error(request, self.error_message)
        return render(request, self.template_name)

    def get(self, request):
        if request.user.is_authenticated:
            return redirect(reverse("homepage"))
        context = {"errors": {}}
        return render(request, self.template_name, context)

    def post(self, request):
        email = request.POST.get("email")
        if not email:
            messages.error(request, "Please enter an email.")
            return render(request, self.template_name, {"errors": {"id_email": "Please enter an email"}})
        else:
            email = email.lower()
            try:
                user = models.User.objects.get(email=email)
                email_handler.send_verification_email(user)
            except models.User.DoesNotExist:
                try:
                    validate_email(email)
                except ValidationError as exc:
                    for errors in exc.error_list:
                        for error in errors:
                            messages.error(request, error)
                    return render(
                        request,
                        self.template_name,
                        {"errors": {"id_email": "Please enter a valid Civil Service email"}},
                    )
                try:
                    restrict_email.clean_email(email=email)
                except ValidationError as exc:
                    for errors in exc.error_list:
                        for error in errors:
                            messages.error(request, error)
                    return render(
                        request,
                        self.template_name,
                        {"errors": {"id_email": "Please enter a valid Civil Service email"}},
                    )

                user = models.User.objects.create_user(email=email)
                email_handler.send_register_email(user)
            return redirect(reverse("email-sent"))


def email_sent_view(request):
    return render(request, "email-sent.html")


def register_email_view(request):
    return verify_email_view(request, register=True)


@require_http_methods(["GET"])
def verify_email_view(request, register=False):
    if request.user.is_authenticated:
        logout(request)
    user_id = request.GET.get("user_id")
    token = request.GET.get("code")
    if not models.User.objects.filter(pk=user_id).exists():
        return render(request, "login-failure.html")
    verify_result = email_handler.verify_token(user_id, token, "email-verification")

    if not verify_result:
        return render(request, "login-failure.html")
    else:
        user = models.User.objects.get(pk=user_id)
        if not user.verified:
            user.verified = True
            user.save()
        login(request, user)
        return redirect(reverse("post-login"))


def post_login_view(request):
    return redirect(reverse("homepage"))


class LogoutView(MethodDispatcher):
    template_name = "logout.html"

    def get(self, request):
        return render(request, self.template_name)

    def post(self, request):
        logout(request)
        return redirect("index")
