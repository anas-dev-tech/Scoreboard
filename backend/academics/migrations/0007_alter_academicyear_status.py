# Generated by Django 5.1.2 on 2024-11-02 20:55

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('academics', '0006_remove_academicyear_is_current_academicyear_status'),
    ]

    operations = [
        migrations.AlterField(
            model_name='academicyear',
            name='status',
            field=models.SmallIntegerField(choices=[(1, 'FINISHED'), (2, 'CURRENT'), (3, 'Upcoming')], default=3),
        ),
    ]