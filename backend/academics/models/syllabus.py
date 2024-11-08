from django.db import models
from django.utils import timezone
from django.core.exceptions import ValidationError
from users.models import Teacher, StudentGroup
from .course import Course
from .academic_year import AcademicYear
from core.constants import Semester

class SyllabusQuerySet(models.QuerySet):
    def get_syllabuses_for_current_semester(self):
        current_year = AcademicYear.objects.get_current_year()
        current_semester = current_year.current_semester
        return self.filter(academic_year=current_year, semester=current_semester)

    def active(self):
        """Return only active (non-deleted) syllabuses."""
        return self.filter(is_deleted=False)

    def soft_delete(self):
        """Soft delete all items in the queryset."""
        return self.update(is_deleted=True, deleted_at=timezone.now())

    def hard_delete(self):
        """Permanently delete all items in the queryset."""
        return super().delete()
    def current(self):
        return self.filter(academic_year=AcademicYear.objects.get_current_year())

class SyllabusManager(models.Manager):
    def get_queryset(self):
        return SyllabusQuerySet(self.model, using=self._db).active().current()

    def copy_syllabus_to_upcoming_year(self, syllabus_id):
        """
        Copy a syllabus to the current academic year with `student_group` set to None.
        """
        syllabus = self.get_queryset().filter(id=syllabus_id, is_deleted=False).first()
        if not syllabus:
            raise ValidationError("Syllabus not found or has been deleted.")

        upcoming_year = AcademicYear.objects.get_upcoming_year()
        
        new_syllabus = Syllabus.objects.create(
            student_group=syllabus.student_group,  # Set student_group to None
            course=syllabus.course,
            teacher=syllabus.teacher,
            academic_year=upcoming_year,
            semester=syllabus.semester,
            quiz_count=syllabus.quiz_count,
        )
        

class Syllabus(models.Model):
    student_group = models.ForeignKey(
        StudentGroup,
        on_delete=models.PROTECT,
        blank=True,
        null=True,
    )  
    course = models.ForeignKey(Course, on_delete=models.PROTECT)
    teacher = models.ForeignKey(Teacher, on_delete=models.PROTECT)
    academic_year = models.ForeignKey(AcademicYear, on_delete=models.PROTECT)    
    semester = models.IntegerField(choices=Semester.choices)
    is_deleted = models.BooleanField(default=False)
    deleted_at = models.DateTimeField(null=True, blank=True)

    objects = SyllabusManager.from_queryset(SyllabusQuerySet)()

    class Meta:
        verbose_name = 'Syllabus'
        verbose_name_plural = 'Syllabuses'
        constraints = [
            models.UniqueConstraint(fields=['student_group', 'course', 'academic_year'], name='unique_curriculum')
        ]

    def __str__(self):
        return f'{self.academic_year} - {self.student_group.name if self.student_group else "No Group"} - {self.course.name}'
    
    def can_add_quiz(self):
        return not self.quizzes_for_this_syllabus.exists() 

    def soft_delete(self):
        """Mark this syllabus as deleted."""
        self.is_deleted = True
        self.deleted_at = timezone.now()
        self.save()

    def hard_delete(self):
        """Permanently delete this syllabus."""
        super(Syllabus, self).delete()
    
    def copy_to_current_year(self):
        """Convenience instance method to copy the syllabus to the current year."""
        return Syllabus.objects.copy_syllabus_to_current_year(self.id)
