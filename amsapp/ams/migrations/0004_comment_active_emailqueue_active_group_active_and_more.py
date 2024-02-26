# Generated by Django 5.0 on 2024-02-24 19:10

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('ams', '0003_user_password_change'),
    ]

    operations = [
        migrations.AddField(
            model_name='comment',
            name='active',
            field=models.BooleanField(default=True),
        ),
        migrations.AddField(
            model_name='emailqueue',
            name='active',
            field=models.BooleanField(default=True),
        ),
        migrations.AddField(
            model_name='group',
            name='active',
            field=models.BooleanField(default=True),
        ),
        migrations.AddField(
            model_name='groupmember',
            name='active',
            field=models.BooleanField(default=True),
        ),
        migrations.AddField(
            model_name='notification',
            name='active',
            field=models.BooleanField(default=True),
        ),
        migrations.AddField(
            model_name='post',
            name='active',
            field=models.BooleanField(default=True),
        ),
        migrations.AddField(
            model_name='reaction',
            name='active',
            field=models.BooleanField(default=True),
        ),
        migrations.AddField(
            model_name='statistic',
            name='active',
            field=models.BooleanField(default=True),
        ),
        migrations.AddField(
            model_name='survey',
            name='active',
            field=models.BooleanField(default=True),
        ),
        migrations.AddField(
            model_name='surveyresponse',
            name='active',
            field=models.BooleanField(default=True),
        ),
    ]
