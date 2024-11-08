# Generated by Django 5.1.2 on 2024-11-04 17:56

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('academics', '0009_syllabus_quiz_count'),
        ('quiz', '0010_remove_quizsession_students_and_more'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='quiz',
            options={'verbose_name': 'Quiz', 'verbose_name_plural': 'Quizzes'},
        ),
        migrations.RemoveField(
            model_name='quiz',
            name='quiz_for',
        ),
        migrations.CreateModel(
            name='QuizSyllabus',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('quiz', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='quiz_syllabuses', to='quiz.quiz')),
                ('syllabus', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='syllabus_quizzes', to='academics.syllabus')),
            ],
        ),
    ]
