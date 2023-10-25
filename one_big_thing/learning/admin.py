from django.conf import settings
from django.contrib import admin
from django_otp.admin import OTPAdminSite
from django_otp.plugins.otp_totp.admin import TOTPDeviceAdmin
from django_otp.plugins.otp_totp.models import TOTPDevice

from one_big_thing.learning.models import Department, User

from . import models


class DepartmentAdmin(admin.ModelAdmin):
    list_display = ["display", "parent", "intranet_url"]
    list_filter = ["parent"]


class SurveyResultAdmin(admin.ModelAdmin):
    readonly_fields = ("id", "modified_at", "created_at")


class UserAdmin(admin.ModelAdmin):
    search_fields = ("email", "first_name", "last_name")
    list_display = ("email", "department")


class OTPAdmin(OTPAdminSite):
    pass


admin_site = OTPAdmin(name="OTPAdmin")
admin_site.register(User, UserAdmin)
admin_site.register(Department, DepartmentAdmin)
admin_site.register(TOTPDevice, TOTPDeviceAdmin)


if settings.DEBUG:
    # we only want to expose a minimum of User data
    # outside of DEBUG mode
    admin_site.register(models.Course)
    admin_site.register(models.Learning)
    admin_site.register(models.SurveyResult, SurveyResultAdmin)
