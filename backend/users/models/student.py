from django.db import models
from core.constants import YearLevel, EducationType, StudentGroupNumber
from django.core.exceptions import ValidationError
from django.db.models import Q

class StudentGroup(models.Model):
    '''Model definition for StudentGroup.'''
    number = models.SmallIntegerField(choices=StudentGroupNumber.choices, default=StudentGroupNumber.GROUP_1)  
    year_level = models.IntegerField(choices=YearLevel.choices)
    major = models.ForeignKey('academics.Major', on_delete=models.CASCADE)
    education_type = models.IntegerField(choices=EducationType.choices)

    
    class Meta:
        '''Meta definition for StudentGroup.'''
        verbose_name = 'Student Group'
        verbose_name_plural = 'Student Groups'
        constraints = [
            models.UniqueConstraint(
                fields=['number', 'year_level', 'major'],
                condition=~Q(year_level=YearLevel.GRADUATED),
                name='unique_student_group'
            )
        ]
    
    
    def __str__(self):
        year_level_str = f'--{self.get_year_level_display()}' if self.year_level == YearLevel.GRADUATED else self.year_level
        return f'{self.major.name}{year_level_str} -- {self.get_number_display()}'


class Student(models.Model):
    '''Model definition for Student.'''
    id = models.IntegerField(primary_key=True)
    name = models.CharField(max_length=100)
    group = models.ForeignKey(
        StudentGroup,
        on_delete=models.CASCADE,
        related_name='students'
    )

    class Meta:
        '''Meta definition for Student.'''

        verbose_name = 'Student'
        verbose_name_plural = 'Students'

    def __str__(self):
        return self.name


