# Generated by Django 5.0 on 2024-02-21 06:34

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('ams', '0002_remove_user_account_status_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='user',
            name='password_change',
            field=models.BooleanField(default=False),
        ),
    ]
