# Generated by Django 3.2.20 on 2023-07-31 16:32

from django.db import migrations


class Migration(migrations.Migration):
    dependencies = [
        ("learning", "0011_auto_20230726_1553"),
    ]

    operations = [
        migrations.RemoveField(
            model_name="user",
            name="has_marked_complete",
        ),
    ]
