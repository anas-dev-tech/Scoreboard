# Generated by Django 5.1.2 on 2024-11-01 21:05

import core.constants
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0009_alter_user_options_alter_user_managers_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='role',
            field=models.SmallIntegerField(choices=core.constants.Role.choices, default=core.constants.Role['TEACHER']),
        ),
    ]
