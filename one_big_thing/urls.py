from django.urls import path
from rest_framework_simplejwt.views import TokenRefreshView

from one_big_thing.learning import (
    authentication_views,
    decorators,
    info_views,
    views,
)
from one_big_thing.learning.admin import admin_site
from one_big_thing.learning.api_views import (
    JwtTokenObtainPairView,
    NormalizedUserStatisticsView,
    UserSignupStatsView,
    UserStatisticsView,
)

api_urlpatterns = [
    path("api/token/", JwtTokenObtainPairView.as_view(), name="token_obtain_pair"),
    path("api/token/refresh/", TokenRefreshView.as_view(), name="token_refresh"),
    path("api/user-statistics/", UserStatisticsView.as_view(), name="user_statistics"),
    path("api/normalized-user-statistics/", NormalizedUserStatisticsView.as_view(), name="normalized_user_statistics"),
    path("api/signup-statistics/", UserSignupStatsView.as_view(), name="signup_statistics"),
]

info_urlpatterns = [
    path("privacy-notice/", info_views.privacy_notice_view, name="privacy-notice"),
    path("accessibility-statement/", info_views.accessibility_statement_view, name="accessibility-statement"),
    path("support/", info_views.support_view, name="support"),
]

admin_urlpatterns = [path("admin/", admin_site.urls)]

other_urlpatterns = [
    path("", authentication_views.CustomLoginView, name="index"),
    path("unauthorised/", decorators.unauthorised_view, name="unauthorised"),
    path("verify-register/", authentication_views.register_email_view, name="verify-email-register"),
    path("verify/", authentication_views.verify_email_view, name="verify-email"),
    path("my-details/", views.MyDetailsView, name="my-details"),
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
    path("feedback/", views.FeedbackView, name="feedback"),
]

urlpatterns = info_urlpatterns + other_urlpatterns + admin_urlpatterns + api_urlpatterns
