from django.db import models
from .major import Major
from django.db.models.functions import Lower
from core.constants import YearLevel, Semester, ResultType, GradeStatus
from django.core.exceptions import ValidationError

class Course(models.Model):
    '''Model definition for Course.'''
    name = models.CharField(max_length=50)
    max_score = models.DecimalField(max_digits=5, decimal_places=2, default=100)
    major = models.ForeignKey(
        Major,
        on_delete=models.CASCADE,
        related_name='courses',
        blank=True,
        null=True
    )
    status = models.SmallIntegerField(choices=GradeStatus.choices, default=GradeStatus.DRAFT)
    year_level = models.SmallIntegerField(choices=YearLevel.choices, default=YearLevel.FIRST_YEAR)
    semester = models.SmallIntegerField(choices=Semester.choices, default=Semester.FIRST_SEMESTER)
    
    class Meta: 
        constraints = [ 
            models.UniqueConstraint(Lower("name"), name="unique_lower_name_course")
        ]
        
    def __str__(self):
        return self.name
    
class GradeType(models.Model):
    course = models.ForeignKey(
        Course,
        on_delete=models.CASCADE,
        related_name='grade_types'
    )
    name = models.CharField(max_length=50)
    max_score = models.DecimalField(max_digits=5, decimal_places=2)
    type = models.SmallIntegerField(choices=ResultType.choices, default=ResultType.NON_QUIZ)
    
    def __str__(self):
        return self.name

    def clean(self):
        if self.type == ResultType.QUIZ and GradeType.objects.filter(course=self.course, type=ResultType.QUIZ).exclude(id=self.id).exists():
            raise ValidationError("A course can only have one quiz result structure.")
        