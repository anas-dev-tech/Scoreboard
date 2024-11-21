from django.db import models


class Major(models.Model):
    '''Model definition for Major.'''    
    name = models.CharField(max_length=50)
    duration_years = models.SmallIntegerField(null=False, blank=False)  # like four year or three years
    
    class Meta:
        '''Meta definition for Major.'''
        verbose_name = 'Major'
        verbose_name_plural = 'Majors'

    def __str__(self):
        return self.name