# Generated by Django 3.2.20 on 2023-08-01 13:00

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("learning", "0012_remove_user_has_marked_complete"),
    ]

    operations = [
        migrations.AlterField(
            model_name="course",
            name="time_to_complete",
            field=models.IntegerField(blank=True, null=True),
        ),
    ]