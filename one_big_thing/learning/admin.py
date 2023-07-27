from django.contrib import admin

from . import models

admin.site.register(models.Course)
admin.site.register(models.Learning)
admin.site.register(models.SurveyResult)
admin.site.register(models.User)
