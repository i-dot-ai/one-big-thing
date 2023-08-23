import logging

from django.contrib import messages
from django.contrib.auth import login
from django.core.exceptions import ValidationError
from django.core.validators import validate_email
from django.shortcuts import redirect, render
from django.urls import reverse
from django.views.decorators.http import require_http_methods

from one_big_thing.learning import (
    choices,
    departments,
    email_handler,
    models,
    restrict_email,
)
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
        context = {"errors": {}}
        return render(request, self.template_name, context)

    def post(self, request):
        email = request.POST.get("email")
        if not email:
            messages.error(request, "Please enter an email.")
            return render(request, self.template_name, {})
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
                    return render(request, self.template_name)
                try:
                    restrict_email.clean_email(email=email)
                except ValidationError as exc:
                    for errors in exc.error_list:
                        for error in errors:
                            messages.error(request, error)
                    return render(request, self.template_name)

                user = models.User.objects.create_user(email=email)
                email_handler.send_register_email(user)
            return redirect(reverse("email-sent"))


def email_sent_view(request):
    return render(request, "email-sent.html")


def register_email_view(request):
    return verify_email_view(request, register=True)


@require_http_methods(["GET"])
def verify_email_view(request, register=False):
    user_id = request.GET.get("user_id")
    token = request.GET.get("code")
    if not models.User.objects.filter(pk=user_id).exists():
        return render(request, "account/verify_email_from_token.html", {"verify_result": False})
    verify_result = email_handler.verify_token(user_id, token, "email-verification")
    if verify_result:
        user = models.User.objects.get(pk=user_id)
        user.verified = True
        user.save()
        user.backend = "django.contrib.auth.backends.ModelBackend"
        login(request, user)
    if register:
        return redirect(reverse("register"))
    else:
        return redirect(reverse("homepage"))


class RegisterView(MethodDispatcher):
    template_name = "register.html"
    error_message = "Something has gone wrong.  Please try again."

    def error(self, request):
        messages.error(request, self.error_message)
        return render(request, self.template_name)

    def get(self, request):
        department_choices = departments.Department.choices
        context = {
            "departments": department_choices,
            "grades": choices.Grade.choices,
            "professions": choices.Profession.choices,
        }
        return render(request, self.template_name, context)

    def post(self, request):
        user = request.user
        department = request.POST.get("department")
        grade = request.POST.get("grade")
        profession = request.POST.get("profession")
        department_choices = departments.Department.choices
        context = {
            "departments": department_choices,
            "grades": choices.Grade.choices,
            "professions": choices.Profession.choices,
        }

        if not department or not grade or not profession:
            if not department:
                messages.error(request, "You must select a department.")
            if not grade:
                messages.error(request, "You must select a grade.")
            if not profession:
                messages.error(request, "You must select a profession.")
            return render(request, self.template_name, context)
        else:
            user.department = department
            user.grade = grade
            user.profession = profession
            user.save()

            return render(
                request,
                "account/signup_complete.html",
                {},
            )
