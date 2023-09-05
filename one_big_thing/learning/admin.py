from django.contrib import admin

from . import models


class SurveyResultAdmin(admin.ModelAdmin):
    readonly_fields = ("id", "modified_at", "created_at")


admin.site.register(models.Course)
admin.site.register(models.Learning)
admin.site.register(models.SurveyResult, SurveyResultAdmin)
admin.site.register(models.User)
