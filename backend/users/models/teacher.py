from django.db import models
from django.contrib.auth import get_user_model
from taggit.managers import TaggableManager
from common.models import CategorizedTaggedItem
User = get_user_model()





class Teacher(models.Model):
    '''Model definition for Teacher.'''
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    tags = TaggableManager(through=CategorizedTaggedItem, verbose_name="Tags", help_text="Add tags for categories like subject, grade, etc.")
    class Meta:
        '''Meta definition for Teacher.'''

        verbose_name = 'Teacher'
        verbose_name_plural = 'Teachers'

    def __str__(self):
        return self.user.name