# Generated by Django 5.1 on 2024-08-27 11:02

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('parkings', '0002_userprofile_parking_limit_history'),
    ]

    operations = [
        migrations.AddField(
            model_name='userprofile',
            name='last_limit_notification_sent',
            field=models.CharField(blank=True, max_length=6, null=True),
        ),
    ]