from django.db import models
from django.contrib.auth import get_user_model
User = get_user_model()





class Teacher(models.Model):
    '''Model definition for Teacher.'''
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    class Meta:
        '''Meta definition for Teacher.'''

        verbose_name = 'Teacher'
        verbose_name_plural = 'Teachers'

    def __str__(self):
        return self.user.first_name + " " + self.user.last_name