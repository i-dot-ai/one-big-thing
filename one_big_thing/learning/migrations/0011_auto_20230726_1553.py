# Generated by Django 3.2.20 on 2023-07-26 15:53

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("learning", "0010_user_profession"),
    ]

    operations = [
        migrations.AlterField(
            model_name="user",
            name="grade",
            field=models.CharField(blank=True, max_length=254, null=True),
        ),
        migrations.AlterField(
            model_name="user",
            name="profession",
            field=models.CharField(blank=True, max_length=254, null=True),
        ),
    ]
