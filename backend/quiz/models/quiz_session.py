from django.db import models
from core.constants import QuizSessionStatus
from users.models import StudentGroup, Student
from django.core.exceptions import ValidationError
from django.utils import timezone

now = timezone.now()

class QuizSession(models.Model):
    '''Model definition for QuizSession.'''
    excluded_students = models.ManyToManyField(
        Student,
        related_name='sessions_excluded',)     
    additional_students = models.ManyToManyField(
        Student,
        )
    date = models.DateTimeField(null=True, blank=True)    
    duration = models.DurationField()
    password = models.CharField(max_length=50, null=False, blank=False)
    status = models.IntegerField(
        choices=QuizSessionStatus,
        default=QuizSessionStatus.UPCOMING
    )
    def __str__(self):
        return self.date.strftime("%d/%m/%Y, %H:%M:%S")
    
    class Meta:
        '''Meta definition for QuizSession.'''

        verbose_name = 'QuizSession'
        verbose_name_plural = 'QuizSessions'

    def clean(self):
        if self.status == QuizSessionStatus.READY:
            if self.date is None:
                raise ValidationError("Date is required for ready sessions")
        
            if self.quizzes.count() == 0:
                raise ValidationError("At least one quiz is required for ready sessions")
            
            if self.quizzes.filter(status__not=QuizSessionStatus.READY).count() == 0:
                raise ValidationError("All quizzes must be ready for ready sessions")
            
            if self.status == QuizSessionStatus.LIVE:
                if self.date is None:
                    raise ValidationError("Date is required for live sessions")
                
                if self.date < now:
                    raise ValidationError("Date must be in the future for live sessions")
            
            
