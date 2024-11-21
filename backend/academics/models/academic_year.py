from django.db import models
from django.core.exceptions import ValidationError
from core.constants import Semester, AcademicYearStatus


class AcademicYearQuerySet(models.QuerySet):
    def get_current_year(self):
        return self.filter(status=AcademicYearStatus.CURRENT).first()





class AcademicYearManager(models.Manager):
    def start_upcoming_year(self):
        current_year = self.get_queryset().get_current_year()
        if current_year:
            current_year.finish_year()  # Calls model method for instance state change
        
        upcoming_year = self.get_queryset().get_upcoming_year()
        if not upcoming_year:
            upcoming_year = self.create_next_year()

        upcoming_year.status = AcademicYearStatus.CURRENT
        upcoming_year.save()
        return upcoming_year

    def create_next_year(self):
        """Helper to create the next academic year based on the current year's end."""
        current_year = self.get_queryset().get_current_year()
        if not current_year:
            raise ValidationError("Cannot create next year without an active current year.")

        return self.create(
            start_year=current_year.end_year,
            end_year=current_year.end_year + 1,
            status=AcademicYearStatus.UPCOMING,
            current_semester=Semester.FIRST_SEMESTER,
        )





class AcademicYear(models.Model):
    start_year = models.IntegerField(help_text="Enter the starting year (e.g., 2023)")
    end_year = models.IntegerField(help_text="Enter the ending year (e.g., 2024)")
    status = models.SmallIntegerField(choices=AcademicYearStatus.choices, default=AcademicYearStatus.CURRENT)
    current_semester = models.SmallIntegerField(choices=Semester.choices, default=Semester.FIRST_SEMESTER)

    objects = AcademicYearManager.from_queryset(AcademicYearQuerySet)()

    class Meta:
        constraints = [
            models.UniqueConstraint(fields=['start_year', 'end_year'], name='unique_academic_year')
        ]

    def clean(self):
        if self.end_year != self.start_year + 1:
            raise ValidationError("The ending year must be one year after the starting year.")

        if self.status == AcademicYearStatus.CURRENT and AcademicYear.objects.filter(status=AcademicYearStatus.CURRENT).exclude(pk=self.pk).exists():
            raise ValidationError("Only one academic year can be marked as current.")
        

    def finish_year(self):
        """Mark the current year as finished."""
        if self.status != AcademicYearStatus.CURRENT:
            raise ValidationError("Only the current academic year can be finished.")

        self.status = AcademicYearStatus.FINISHED
        self.save()
    
    def __str__(self):
        return f"{self.start_year}-{self.end_year}"
