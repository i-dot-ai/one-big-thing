from django.contrib import admin
from django_otp.admin import OTPAdminSite
from django.contrib.auth.models import User
from django_otp.plugins.otp_totp.models import TOTPDevice
from django_otp.plugins.otp_totp.admin import TOTPDeviceAdmin

from . import models


class SurveyResultAdmin(admin.ModelAdmin):
    readonly_fields = ("id", "modified_at", "created_at")


class OTPAdmin(OTPAdminSite):
    pass


admin_site = OTPAdmin(name='OTPAdmin')
admin_site.register(User)
admin.site.register(models.Course)
admin.site.register(models.Learning)
admin.site.register(models.SurveyResult, SurveyResultAdmin)
admin_site.register(TOTPDevice, TOTPDeviceAdmin)







