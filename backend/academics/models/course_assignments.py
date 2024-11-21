from django.db import models
from django.utils import timezone
from django.core.exceptions import ValidationError
from users.models import Teacher, StudentGroup
from .course import Course
from .academic_year import AcademicYear
from core.constants import Semester

        

class CourseAssignment(models.Model):
    student_group = models.ForeignKey(
        StudentGroup,
        on_delete=models.PROTECT,
        related_name='course_assignments',
        blank=True,
        null=True,
    )  
    course = models.ForeignKey(
        Course,
        on_delete=models.PROTECT,
        related_name='course_assignments'
    )
    teacher = models.ForeignKey(
        Teacher,
        on_delete=models.PROTECT,
        related_name='assigned_courses'
    )



    class Meta:
        verbose_name = 'Course Assignment'
        verbose_name_plural = 'Course Assignments'
        
        constraints = [
            models.UniqueConstraint(fields=['student_group', 'course'], name='unique_student_group_course')
        ]

    def __str__(self):
        return f'{self.student_group.number if self.student_group else "No Group"} - {self.course.name}'
    
    def can_add_quiz(self):
        return not self.quizzes_for_this_syllabus.exists() 
