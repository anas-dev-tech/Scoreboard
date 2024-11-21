# Generated by Django 5.1.2 on 2024-11-19 22:48

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('academics', '0002_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='grade',
            name='academic_year',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, related_name='grades', to='academics.academicyear'),
            preserve_default=False,
        ),
    ]
