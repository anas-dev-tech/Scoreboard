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
    answer= models.OneToOneField(
        "QuestionOption",
        on_delete=models.CASCADE,
        related_name='question_answer',
        blank=True,
        null=True
    )    
    score = models.DecimalField(max_digits=4, decimal_places=2)
    question_difficulty = models.SmallIntegerField(
        choices=QuestionDifficulty.choices,
        default=QuestionDifficulty.EASY
    )
    
    question_type = models.IntegerField(
        choices=QuestionType.choices,
        default=QuestionType.MULTIPLE_CHOICE
    )

    def __str__(self):
        return self.text

    def is_true_or_false_question(self):
        return self.question_type == QuestionType.TRUE_OR_FALSE

    def is_multiple_choice_question(self):
        return self.question_type == QuestionType.MULTIPLE_CHOICE

class QuestionOption(models.Model):
    text = models.CharField(max_length=50, null=False, blank=False)
    question = models.ForeignKey(
        Question,
        on_delete=models.CASCADE,
        related_name='question_options'
    )
    
    def __str__(self):
        return self.text
    
