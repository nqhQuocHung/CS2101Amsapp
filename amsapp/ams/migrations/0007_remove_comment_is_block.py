# Generated by Django 5.0 on 2024-02-25 18:14

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('ams', '0006_comment_is_block'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='comment',
            name='is_block',
        ),
    ]
