# Generated by Django 3.2.20 on 2023-07-12 11:20

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('learning', '0002_auto_20230711_1312'),
    ]

    operations = [
        migrations.AddField(
            model_name='user',
            name='last_token_sent_at',
            field=models.DateTimeField(blank=True, editable=False, null=True),
        ),
    ]
