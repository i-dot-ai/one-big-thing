from django.conf import settings
from django.contrib import admin
from django.urls import path

from one_big_thing.learning import (
    authentication_views,
    decorators,
    info_views,
    views,
)

info_urlpatterns = [
    path("privacy-notice/", info_views.privacy_notice_view, name="privacy-notice"),
    path("accessibility-statement/", info_views.accessibility_statement_view, name="accessibility-statement"),
    path("support/", info_views.support_view, name="support"),
]

admin_urlpatterns = [path("admin/", admin.site.urls)]

other_urlpatterns = [
    path("", authentication_views.CustomLoginView, name="index"),
    path("unauthorised/", decorators.unauthorised_view, name="unauthorised"),
    path("verify-register/", authentication_views.register_email_view, name="verify-email-register"),
    path("verify/", authentication_views.verify_email_view, name="verify-email"),
    path("register/", views.RegisterView, name="register"),
    path("logout/", authentication_views.LogoutView, name="logout"),
    path("email-sent/", authentication_views.email_sent_view, name="email-sent"),
    path("post-login/", authentication_views.post_login_view, name="post-login"),
    path("home/", views.homepage_view, name="homepage"),
    path("record-learning/", views.RecordLearningView, name="record-learning"),
    path("record-learning/<uuid:course_id>/", views.RecordLearningView, name="record-learning"),
    path("questions/<str:survey_type>/", views.questions_view, name="questions"),
    path("questions/<str:survey_type>/<int:page_number>/", views.questions_view, name="questions"),
    path("complete-hours/", views.complete_hours_view, name="complete-hours"),
    path("send-learning-record/", views.send_learning_record_view, name="send-learning-record"),
    path("delete-learning-check/<uuid:learning_id>/", views.check_delete_learning_view, name="delete-learning-check"),
    path("additional-learning/", views.additional_learning_view, name="additional-learning"),
    path("intro-pre-survey/", views.intro_to_pre_survey_view, name="intro-pre-survey"),
    path("end-pre-survey/", views.end_pre_survey_view, name="end-pre-survey"),
    path("intro-post-survey/", views.intro_to_post_survey_view, name="intro-post-survey"),
    path("end-post-survey/", views.end_post_survey_view, name="end-post-survey"),
    path("department-links/", views.department_links_view, name="department-links"),
]

urlpatterns = info_urlpatterns + other_urlpatterns

if settings.DEBUG:
    urlpatterns = urlpatterns + admin_urlpatterns
