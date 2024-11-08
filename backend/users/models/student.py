from django.db import models
from core.constants import YearLevel, EducationType
from django.core.exceptions import ValidationError
    
    
class StudentGroup(models.Model):
    '''Model definition for StudentGroup.'''
    name = models.CharField(max_length=100)
    year_level = models.IntegerField(choices=YearLevel.choices)
    major = models.ForeignKey('academics.Major', on_delete=models.CASCADE)
    education_type = models.IntegerField(choices=EducationType.choices)
    
    def clean(self):
        if self.year_level > self.major.duration_years:
            raise ValidationError("Year of subject cannot be greater than the max year in the major")

    def __str__(self):
        return f'{self.major.name}-{self.year_level} --- {self.name}'


class Student(models.Model):
    '''Model definition for Student.'''
    id = models.IntegerField(primary_key=True)
    name = models.CharField(max_length=100)
    group = models.ForeignKey(StudentGroup, on_delete=models.CASCADE, default=1)

    class Meta:
        '''Meta definition for Student.'''

        verbose_name = 'Student'
        verbose_name_plural = 'Students'

    def __str__(self):
        return self.name

