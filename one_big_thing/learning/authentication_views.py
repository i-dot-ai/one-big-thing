from datetime import datetime
from urllib.parse import urlencode

from allauth.account.views import SignupView
from django.contrib import messages
from django.contrib.auth import authenticate, login
from django.contrib.auth.password_validation import validate_password
from django.core.exceptions import ValidationError
from django.core.validators import validate_email
from django.shortcuts import redirect, render
from django.urls import reverse
from django.views.decorators.http import require_http_methods

from one_big_thing import settings
from one_big_thing.learning import email_handler, models, restrict_email
from one_big_thing.learning.email_handler import (
    send_account_already_exists_email,
)
from one_big_thing.learning.utils import MethodDispatcher


@require_http_methods(["GET", "POST"])
class CustomLoginView(MethodDispatcher):
    def get(self, request):
        return render(request, "account/login.html")

    def post(self, request):
        password = request.POST.get("password", None)
        email = request.POST.get("login", None)
        if not password or not email:
            messages.error(request, "Please enter an email and password.")
            return render(request, "account/login.html", {})
        else:
            user = authenticate(request, email=email, password=password)
            if user is not None:
                if settings.SEND_VERIFICATION_EMAIL:
                    if not user.verified:
                        return render(
                            request, "account/login.html", {"resend_verification": True, "resend_email": user.email}
                        )
                login(request, user)
                request.session["session_created_at"] = datetime.now().strftime("%Y-%m-%dT%H:%M:%S")
                return redirect("index")
            else:
                messages.error(request, "The email address or password you entered is incorrect. Please try again.")
                return render(request, "account/login.html", {})


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
    def dispatch(self, request, *args, **kwargs):
        if request.method == "POST":
            email = request.POST.get("email")
            password1 = request.POST.get("password1")
            password2 = request.POST.get("password2")
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
            try:
                validate_password(password1)
            except ValidationError as exc:
                for errors in exc.error_list:
                    for error in errors:
                        messages.error(request, error)
                return render(request, self.template_name)
            if password1 != password2:
                messages.error(request, "You must type the same password each time.")
                return render(request, self.template_name)
            existing_user = models.User.objects.filter(email=email)
            if existing_user.exists():
                send_account_already_exists_email(existing_user.first())
                return render(
                    request,
                    "account/signup_complete.html",
                    {},
                )
            user = models.User.objects.create_user(email=email, password=password1)
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
        response = super().dispatch(request, *args, **kwargs)
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
        return render(request, "account/verify_email_from_token.html", {"verify_result": verify_result})


@require_http_methods(["GET", "POST"])
class PasswordReset(MethodDispatcher):
    def get(self, request):
        return render(request, "account/password_reset.html", {})

    def post(self, request):
        email = request.POST.get("email")
        try:
            user = models.User.objects.get(email=email)
        except models.User.DoesNotExist:
            return render(request, "account/password_reset_done.html", {})
        email_handler.send_password_reset_email(user)
        return render(request, "account/password_reset_done.html", {})


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
class AcceptInviteSignupView(MethodDispatcher):
    password_signup_error_message = (
        "This link is not valid. It may have expired or have already been used. Please request another one."
    )

    def get_token_request_args(self, request):
        user_id = request.GET.get("user_id", None)
        token = request.GET.get("code", None)
        valid_request = False
        if not user_id or not token:
            messages.error(request, self.password_signup_error_message)
            return user_id, token, valid_request
        else:
            result = email_handler.verify_token(user_id, token, "invite-user")
            if not result:
                messages.error(request, self.password_signup_error_message)
                return user_id, token, valid_request
            else:
                valid_request = True
        return user_id, token, valid_request

    def get(self, request):
        contact_email = settings.CONTACT_EMAIL
        try:
            _, _, valid_request = self.get_token_request_args(request)
            return render(
                request, "account/accept_signup_invite.html", {"valid": valid_request, "contact_address": contact_email}
            )
        except models.User.DoesNotExist:
            return render(
                request, "account/accept_signup_invite.html", {"valid": False, "contact_address": contact_email}
            )

    def post(self, request):
        user_id, token, valid_request = self.get_token_request_args(request)
        pwd1 = request.POST.get("password1", None)
        pwd2 = request.POST.get("password2", None)
        if pwd1 != pwd2:
            messages.error(request, "Passwords must match.")
            query_params = urlencode({"user_id": user_id, "code": token})
            redirect_url = reverse("accept-invite") + "?" + query_params
            response = redirect(redirect_url)
            messages.middleware.MessageMiddleware().process_response(request, response)
            return response
        if not valid_request:
            messages.error(request, self.password_signup_error_message)
            query_params = urlencode({"user_id": user_id, "code": token})
            redirect_url = reverse("accept-invite") + "?" + query_params
            response = redirect(redirect_url)
            messages.middleware.MessageMiddleware().process_response(request, response)
            return response
        user = models.User.objects.get(pk=user_id)
        try:
            validate_password(pwd1, user)
        except ValidationError as e:
            for msg in e:
                messages.error(request, str(msg))
            query_params = urlencode({"user_id": user_id, "code": token})
            redirect_url = reverse("accept-invite") + "?" + query_params
            response = redirect(redirect_url)
            messages.middleware.MessageMiddleware().process_response(request, response)
            return response
        user.set_password(pwd1)
        user.invite_accepted_at = datetime.now()
        user.verified = True
        user.save()
        return render(request, "account/accept_signup_invite_done.html", {})
