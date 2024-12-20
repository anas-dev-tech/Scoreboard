# Generated by Django 5.1.2 on 2024-11-19 21:48

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('academics', '0001_initial'),
        ('auth', '0012_alter_user_first_name_max_length'),
    ]

    operations = [
        migrations.CreateModel(
            name='User',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('password', models.CharField(max_length=128, verbose_name='password')),
                ('last_login', models.DateTimeField(blank=True, null=True, verbose_name='last login')),
                ('is_superuser', models.BooleanField(default=False, help_text='Designates that this user has all permissions without explicitly assigning them.', verbose_name='superuser status')),
                ('email', models.EmailField(max_length=254, unique=True)),
                ('role', models.SmallIntegerField(choices=[(1, 'Admin'), (2, 'Teacher')], default=2)),
                ('is_staff', models.BooleanField(default=False)),
                ('is_active', models.BooleanField(default=True)),
                ('date_joined', models.DateTimeField(auto_now_add=True)),
                ('force_change_password', models.BooleanField(default=False)),
                ('first_name', models.CharField(blank=True, max_length=30)),
                ('last_name', models.CharField(blank=True, max_length=30)),
                ('groups', models.ManyToManyField(blank=True, help_text='The groups this user belongs to. A user will get all permissions granted to each of their groups.', related_name='user_set', related_query_name='user', to='auth.group', verbose_name='groups')),
                ('user_permissions', models.ManyToManyField(blank=True, help_text='Specific permissions for this user.', related_name='user_set', related_query_name='user', to='auth.permission', verbose_name='user permissions')),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='StudentGroup',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('number', models.SmallIntegerField(choices=[(1, 'Group 1'), (2, 'Group 2'), (3, 'Group 3'), (4, 'Group 4'), (5, 'Group 5')], default=1)),
                ('year_level', models.IntegerField(choices=[(1, 'First Year'), (2, 'Second Year'), (3, 'Third Year'), (4, 'Fourth Year'), (5, 'Fifth Year'), (6, 'Graduated')])),
                ('education_type', models.IntegerField(choices=[(0, 'Male Only'), (1, 'Female Only'), (2, 'Co-education')])),
                ('major', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='academics.major')),
            ],
            options={
                'verbose_name': 'Student Group',
                'verbose_name_plural': 'Student Groups',
            },
        ),
        migrations.CreateModel(
            name='Student',
            fields=[
                ('id', models.IntegerField(primary_key=True, serialize=False)),
                ('name', models.CharField(max_length=100)),
                ('group', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='students', to='users.studentgroup')),
            ],
            options={
                'verbose_name': 'Student',
                'verbose_name_plural': 'Students',
            },
        ),
        migrations.CreateModel(
            name='Teacher',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'verbose_name': 'Teacher',
                'verbose_name_plural': 'Teachers',
            },
        ),
        migrations.AddConstraint(
            model_name='studentgroup',
            constraint=models.UniqueConstraint(condition=models.Q(('year_level', 6), _negated=True), fields=('number', 'year_level', 'major'), name='unique_student_group'),
        ),
    ]
