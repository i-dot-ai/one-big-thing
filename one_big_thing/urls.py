from django.conf import settings
from django.contrib import admin
from django.urls import include, path

from one_big_thing.learning import views

allauth_urlpatterns = [
    path("accounts/", include("allauth.urls")),
]
admin_urlpatterns = [
    path("admin/", admin.site.urls),
]

other_urlpatterns = [
    path("", views.index_view, name="index"),
    path("home/", views.homepage_view, name="homepage"),
]

urlpatterns = allauth_urlpatterns + other_urlpatterns

if settings.DEBUG:
    urlpatterns = urlpatterns + admin_urlpatterns
