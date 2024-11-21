from django.db import models
from users.models import Student
from academics.models import CourseAssignment
from .question import Question, QuestionOption
from core.constants import QuizStudentStatus

class QuizStudent(models.Model):
    student = models.ForeignKey(
        Student,
        on_delete=models.CASCADE
    )
    
    syllabus = models.ForeignKey(
        CourseAssignment,
        on_delete=models.CASCADE,
    )
    
    score = models.IntegerField(
        null=True,
        blank=True,
    )
    
    status = models.SmallIntegerField(
        choices=QuizStudentStatus.choices,
        db_default=QuizStudentStatus.UPCOMING
    )
    
    

class QuizStudentQuestion(models.Model):
    quiz_student = models.ForeignKey(
        QuizStudent,
        on_delete=models.CASCADE
    )
    
    question = models.ForeignKey(
        Question,
        on_delete=models.CASCADE
    )
    
    answer = models.ForeignKey(
        QuestionOption,
        on_delete=models.CASCADE,
        null=True,
        blank=True,
    )
    