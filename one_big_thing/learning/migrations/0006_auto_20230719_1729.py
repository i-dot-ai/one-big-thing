# Generated by Django 3.2.20 on 2023-07-19 17:29

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("learning", "0005_surveyresult"),
    ]

    operations = [
        migrations.AddField(
            model_name="user",
            name="has_completed_post_survey",
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name="user",
            name="has_completed_pre_survey",
            field=models.BooleanField(default=False),
        ),
    ]
