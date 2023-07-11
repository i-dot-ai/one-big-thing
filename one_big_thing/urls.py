from django.conf import settings
from django.contrib import admin
from django.urls import include, path

from one_big_thing.learning import authentication_views, views

account_urlpatterns = [
    path("accounts/verify/", authentication_views.CustomVerifyUserEmail, name="verify-email"),
    path("accounts/password-reset/", authentication_views.PasswordReset, name="password-reset"),
    path("accounts/change-password/reset/", authentication_views.PasswordChange, name="password-set"),
    path("accounts/login/", authentication_views.CustomLoginView, name="account_login"),
    path("accounts/signup/", authentication_views.CustomSignupView.as_view(), name="account_signup"),
    path("accounts/verify/resend/", authentication_views.CustomResendVerificationView, name="resend-verify-email"),
    path("accounts/accept-invite/", authentication_views.AcceptInviteSignupView, name="accept-invite"),
    path("accounts/", include("allauth.urls")),
]

admin_urlpatterns = [
    path("admin/", admin.site.urls),
]

other_urlpatterns = [
    path("", views.index_view, name="index"),
    path("home/", views.homepage_view, name="homepage"),
    path("record-learning/", views.RecordLearningView, name="record-learning"),
    path("test/", views.test_view, name="test"),
]

urlpatterns = account_urlpatterns + other_urlpatterns

if settings.DEBUG:
    urlpatterns = urlpatterns + admin_urlpatterns
