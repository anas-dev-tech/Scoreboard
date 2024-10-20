from django.db import models
from taggit.managers import TaggableManager
from common.models import CategorizedTaggedItem



class Quiz(models.Model):
    name = models.CharField(max_length=120)
    time = models.IntegerField(help_text="duration of the quiz in minutes")
    number_of_questions = models.IntegerField()
    required_score_to_pass = models.IntegerField(help_text="required score in %")
    teachers_in_charge = models.ManyToManyField('users.Teacher', related_name='quizzes_in_charge')
    # Field to indicate if the quiz is randomized for each student
    is_randomized = models.BooleanField(default=False)

    # Fields for specifying the number of questions, only relevant if the quiz is randomized
    easy_questions_count = models.IntegerField(default=0)
    medium_questions_count = models.IntegerField(default=0)
    hard_questions_count = models.IntegerField(default=0)
    tags = TaggableManager(through=CategorizedTaggedItem, verbose_name="Tags", help_text="Add tags for categories like subject, grade, etc.")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    
    def __str__(self):
        return self.name