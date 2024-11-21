from django.db import models
from .course import GradeType, Course
from .major import Major
from .academic_year import AcademicYear
from core.constants import YearLevel
from users.models import Student
from django.core.exceptions import ValidationError


class Grade(models.Model):
    student = models.ForeignKey(
        Student,
        on_delete=models.CASCADE,
        related_name='grades'
    )
    course = models.ForeignKey(
        Course,
        on_delete=models.PROTECT,
        related_name='grades',
    )
    major = models.ForeignKey(Major, on_delete=models.PROTECT)
    year_level = models.SmallIntegerField(
        choices=YearLevel.choices,
        default=YearLevel.FIRST_YEAR
    )
    semester = models.CharField(max_length=10)
    score = models.DecimalField(max_digits=5, decimal_places=2, default=0)
    max_score = models.DecimalField(max_digits=5, decimal_places=2, db_default=100)
    academic_year = models.ForeignKey(
        AcademicYear, 
        on_delete=models.CASCADE,
        related_name="grades"
    )
    
    def clean(self):
        if self.score > self.max_score:
            raise ValidationError("Score cannot be greater than max score.")


class GradeDetail(models.Model):
    grade = models.ForeignKey(
        Grade,
        on_delete=models.CASCADE,
        related_name= "grade_details",
    )
    type = models.ForeignKey(
        GradeType,
        on_delete=models.CASCADE,
    )
    score = models.DecimalField(decimal_places=2, max_digits=5, default=0)
    max_score = models.DecimalField(max_digits=5, decimal_places=2, db_default=100)
    
    
    def clean(self):
        if self.score > self.max_score:
            raise ValidationError("Score cannot be greater than max score.")
        
        if GradeDetail.objects.filter(course_result=self.course_result).aggregate(models.Sum('max_score'))['max_score__sum'] > self.course_result.max_score:
            raise ValidationError("Total max score of grade details cannot be greater than max score of the course result.")
