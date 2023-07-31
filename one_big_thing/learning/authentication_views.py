import logging
from datetime import datetime

from allauth.account.views import SignupView
from django.conf import settings
from django.contrib import messages
from django.contrib.auth import authenticate, login
from django.contrib.auth.password_validation import validate_password
from django.core.exceptions import ValidationError
from django.core.validators import validate_email
from django.shortcuts import redirect, render
from django.views.decorators.http import require_http_methods

from one_big_thing.learning import (
    choices,
    departments,
    email_handler,
    models,
    restrict_email,
)
from one_big_thing.learning.email_handler import (
    send_account_already_exists_email,
)
from one_big_thing.learning.utils import MethodDispatcher

logger = logging.getLogger(__name__)


def _strip_microseconds(dt):
    if not dt:
        return None
    return dt.replace(microsecond=0, tzinfo=None)


@require_http_methods(["GET", "POST"])
class CustomLoginView(MethodDispatcher):
    template_name = "account/login.html"
    error_message = "Something has gone wrong.  Please contact an admin."

    def error(self, request):
        messages.error(request, self.error_message)
        return render(request, self.template_name)

    def get(self, request):
        return render(request, self.template_name)

    def post(self, request):
        password = request.POST.get("password", None)
        email = request.POST.get("login", None)
        if not password or not email:
            messages.error(request, "Please enter an email and password.")
            return render(request, self.template_name, {})
        else:
            email = email.lower()
            user = authenticate(request, email=email, password=password)
            if user is not None:
                if settings.SEND_VERIFICATION_EMAIL:
                    if not user.verified:
                        return render(
                            request, "account/login.html", {"resend_verification": True, "resend_email": user.email}
                        )
                login(request, user)
                request.session["session_created_at"] = datetime.now().strftime("%Y-%m-%dT%H:%M:%S")
                if not request.user.has_completed_pre_survey:
                    return redirect("questions", "pre")
                return redirect("index")
            else:
                return self.error(request)


@require_http_methods(["GET", "POST"])
class CustomResendVerificationView(MethodDispatcher):
    def get(self, request):
        email = request.GET.get("email")
        if not email:
            return render(request, "account/resend_verification_email.html", {})
        else:
            user = models.User.objects.filter(email=email).first()
            if not user:
                return render(request, "account/resend_verification_email.html", {})
            email_handler.send_verification_email(user)
            return render(
                request,
                "account/signup_complete.html",
                {},
            )

    def post(self, request):
        email = request.POST.get("email")
        if not email:
            messages.error(request, "Please enter a valid email address.")
            return render(request, "account/resend_verification_email.html", {})
        try:
            validate_email(email)
        except ValidationError as exc:
            for errors in exc.error_list:
                for error in errors:
                    messages.error(request, error)
            return render(request, "account/resend_verification_email.html", {})
        try:
            restrict_email.clean_email(email=email)
        except ValidationError as exc:
            for errors in exc.error_list:
                for error in errors:
                    messages.error(request, error)
            return render(request, "account/resend_verification_email.html", {})
        user = models.User.objects.filter(email=email).first()
        if user:
            email_handler.send_verification_email(user)
        return render(request, "account/signup_complete.html", {})


class CustomSignupView(SignupView):
    def get_context_data(self, **kwargs):
        department_choices = departments.Department.choices
        context = super(CustomSignupView, self).get_context_data(**kwargs)
        context["departments"] = department_choices
        context["grades"] = choices.Grade.choices
        context["professions"] = choices.Profession.choices
        return context

    def dispatch(self, request, *args, **kwargs):
        if request.method == "POST":
            email = request.POST.get("email")
            password1 = request.POST.get("password1")
            password2 = request.POST.get("password2")
            department = request.POST.get("department")
            grade = request.POST.get("grade")
            profession = request.POST.get("profession")
            context = {
                "departments": departments.Department.choices,
                "grades": choices.Grade.choices,
                "professions": choices.Profession.choices,
            }
            try:
                validate_email(email)
            except ValidationError as exc:
                for errors in exc.error_list:
                    for error in errors:
                        messages.error(request, error)
                return render(request, self.template_name, context)
            try:
                restrict_email.clean_email(email=email)
            except ValidationError as exc:
                for errors in exc.error_list:
                    for error in errors:
                        messages.error(request, error)
                return render(request, self.template_name, context)
            try:
                validate_password(password1)
            except ValidationError as exc:
                for errors in exc.error_list:
                    for error in errors:
                        messages.error(request, error)
                return render(request, self.template_name, context)
            if password1 != password2:
                messages.error(request, "You must type the same password each time.")
                return render(request, self.template_name, context)
            existing_user = models.User.objects.filter(email=email)
            if existing_user.exists():
                send_account_already_exists_email(existing_user.first())
                return render(
                    request,
                    "account/signup_complete.html",
                    {},
                )
            if not department or not grade or not profession:
                if not department:
                    messages.error(request, "You must select a department.")
                if not grade:
                    messages.error(request, "You must select a grade.")
                if not profession:
                    messages.error(request, "You must select a profession.")
                return render(request, self.template_name, context)
            user = models.User.objects.create_user(
                email=email, password=password1, department=department, grade=grade, profession=profession
            )
            user.save()
            if settings.SEND_VERIFICATION_EMAIL:
                email_handler.send_verification_email(user)
                return render(
                    request,
                    "account/signup_complete.html",
                    {},
                )
            user = authenticate(request, email=email, password=password1)
            login(request, user)
            messages.success(request, f"Successfully signed in as {user.email}.")
            return redirect("index")
        response = super().dispatch(request, errors={}, *args, **kwargs)
        return response


@require_http_methods(["GET"])
class CustomVerifyUserEmail(MethodDispatcher):
    def get(self, request):
        user_id = request.GET.get("user_id")
        token = request.GET.get("code")
        if not models.User.objects.filter(pk=user_id).exists():
            return render(request, "account/verify_email_from_token.html", {"verify_result": False})
        verify_result = email_handler.verify_token(user_id, token, "email-verification")
        if verify_result:
            user = models.User.objects.get(pk=user_id)
            user.verified = True
            user.save()
            login(request, user, backend="django.contrib.auth.backends.ModelBackend")
            return redirect("index")
        return render(request, "account/verify_email_from_token.html", {"verify_result": verify_result})


@require_http_methods(["GET", "POST"])
class PasswordChange(MethodDispatcher):
    password_reset_error_message = (
        "This link is not valid. It may have expired or have already been used. Please try again."
    )

    def get_token_request_args(self, request):
        user_id = request.GET.get("user_id", None)
        token = request.GET.get("code", None)
        valid_request = False
        if not user_id or not token:
            messages.error(request, self.password_reset_error_message)
        else:
            result = email_handler.verify_token(user_id, token, "password-reset")
            if not result:
                messages.error(request, self.password_reset_error_message)
            else:
                valid_request = True
        return user_id, token, valid_request

    def get(self, request):
        try:
            _, _, valid_request = self.get_token_request_args(request)
            return render(request, "account/password_reset_from_key.html", {"valid": valid_request})
        except models.User.DoesNotExist:
            return render(request, "account/password_reset_from_key.html", {"valid": False})

    def post(self, request):
        user_id, token, valid_request = self.get_token_request_args(request)
        pwd1 = request.POST.get("password1", None)
        pwd2 = request.POST.get("password2", None)
        if pwd1 != pwd2:
            messages.error(request, "Passwords must match.")
            return render(request, "account/password_reset_from_key.html", {"valid": valid_request})
        if not valid_request:
            messages.error(request, self.password_reset_error_message)
            return render(request, "account/password_reset_from_key.html", {"valid": valid_request})
        user = models.User.objects.get(pk=user_id)
        try:
            validate_password(pwd1, user)
        except ValidationError as e:
            for msg in e:
                messages.error(request, str(msg))
            return render(request, "account/password_reset_from_key.html", {"valid": valid_request})
        user.set_password(pwd1)
        user.save()
        return render(request, "account/password_reset_from_key_done.html", {})


@require_http_methods(["GET", "POST"])
class PasswordReset(MethodDispatcher):
    def get(self, request):
        return render(request, "account/password_reset.html", {})

    def post(self, request):
        email = request.POST.get("email")
        try:
            user = models.User.objects.get(email=email)
        except models.User.DoesNotExist:
            return redirect("password-reset-done")
        email_handler.send_password_reset_email(user)
        return redirect("password-reset-done")


@require_http_methods(["GET"])
def password_reset_done(request):
    return render(request, "account/password_reset_done.html", {})


@require_http_methods(["GET"])
def password_reset_from_key_done(request):
    return render(request, "account/password_reset_from_key_done.html", {})
