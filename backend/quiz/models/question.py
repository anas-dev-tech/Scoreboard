from django.db import models
from core.constants import QuestionType, QuestionDifficulty
from django.core.exceptions import ValidationError

class Question(models.Model):
    text = models.CharField(
        max_length=50,
        null=False,
        blank=False
    )
    
    quiz = models.ForeignKey(
        "quiz.Quiz",
        on_delete=models.CASCADE,
        related_name='quiz_questions'
    )    
    score = models.DecimalField(max_digits=4, decimal_places=2)


    def __str__(self):
        return self.text
    
    def answer(self):
        return self.question_options.filter(is_correct=True).first()

class QuestionOption(models.Model):
    text = models.CharField(max_length=50, null=False, blank=False)
    question = models.ForeignKey(
        Question,
        on_delete=models.CASCADE,
        related_name='question_options'
    )
    is_correct = models.BooleanField(default=False)

    def __str__(self):
        return self.text
    
