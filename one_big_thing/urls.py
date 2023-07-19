from django.conf import settings
from django.contrib import admin
from django.urls import include, path

from one_big_thing.learning import authentication_views, views

account_urlpatterns = [
    path("accounts/verify/", authentication_views.CustomVerifyUserEmail, name="verify-email"),
    path("accounts/password-reset/", authentication_views.PasswordReset, name="password-reset"),
    path("accounts/change-password/reset/", authentication_views.PasswordChange, name="password-set"),
    path("accounts/password-reset-done/", authentication_views.password_reset_done, name="password-reset-done"),
    path(
        "accounts/password-reset-from-key-done/",
        authentication_views.password_reset_from_key_done,
        name="password-reset-from-key-done",
    ),
    path("accounts/login/", authentication_views.CustomLoginView, name="account_login"),
    path("accounts/signup/", authentication_views.CustomSignupView.as_view(), name="account_signup"),
    path("accounts/verify/resend/", authentication_views.CustomResendVerificationView, name="resend-verify-email"),
    path("accounts/", include("allauth.urls")),
]

admin_urlpatterns = [
    path("admin/", admin.site.urls),
]

other_urlpatterns = [
    path("", views.index_view, name="index"),
    path("home/", views.homepage_view, name="homepage"),
    path("record-learning/", views.RecordLearningView, name="record-learning"),
    path("record-learning/<uuid:course_id>", views.RecordLearningView, name="record-learning"),
    path("questions/<str:survey_type>/", views.questions_view, name="questions"),
    path("questions/<str:survey_type>/<int:page_number>/", views.questions_view, name="questions"),
    path("completed", views.survey_completed_view, name="survey-completed"),
    path("complete-hours/", views.complete_hours_view, name="complete-hours"),
    path("test/", views.test_view, name="test"),
]

urlpatterns = account_urlpatterns + other_urlpatterns

if settings.DEBUG:
    urlpatterns = urlpatterns + admin_urlpatterns
