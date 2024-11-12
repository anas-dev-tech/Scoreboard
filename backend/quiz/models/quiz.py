from django.db import models
from django.core.exceptions import ValidationError
from academics.models import Syllabus
from core.constants import QuizStatus, AcademicYearStatus
from .quiz_session import QuizSession
from icecream import ic


class QuizQuerySet(models.QuerySet):
    def create_quizzes_for_syllabuses(self, syllabus_ids):
        # Fetch selected syllabuses
        syllabuses = Syllabus.objects.filter(id__in=syllabus_ids)
        quizzes = []
        
        for syllabus in syllabuses:
            # Check if the syllabus allows adding more quizzes
            if not syllabus.can_add_quiz():
                raise ValidationError(f"Cannot add more quizzes for syllabus: {syllabus}")
            
            # Create the quiz with syllabus details and nullify the student group
            quiz = self.create(
                title=f"Quiz for {syllabus.course.name} - {syllabus.student_group or 'General'}",
                time=90,
                number_of_questions=10,
                required_score_to_pass=50,
                is_randomized=False,
                easy_questions_count=0,
                medium_questions_count=0,
                hard_questions_count=0,
                quiz_session=None,
                status=QuizStatus.DRAFT,
            )
            quiz.quiz_for.add(syllabus)  # Add syllabus to ManyToManyField
            quizzes.append(quiz)
        
        return quizzes  # Return list of created quizzes
    
    def publish_quizzes(self, quiz_ids):
        # Fetch selected quizzes
        quizzes = self.filter(id__in=quiz_ids)
        published_quizzes = []
        
        for quiz in quizzes:
            # Check if the quiz can be published
            if not quiz.can_publish():
                raise ValidationError(f"Cannot publish quiz: {quiz}")
            
            # Publish the quiz
            quiz.status = QuizStatus.PUBLISHED
            quiz.save()
            published_quizzes.append(quiz)
    def get_quizzes_for_teacher(self, teacher_id):
        syllabuses = Syllabus.objects.filter(teacher__id=teacher_id)
        ic(syllabuses)
        
        teacher_quizzes = self.filter(quiz_for__in=syllabuses)
        return teacher_quizzes



class Quiz(models.Model):
    title = models.CharField(max_length=120, blank=True)
    time = models.IntegerField(default=90)
    number_of_questions = models.IntegerField(default=20, blank=True)
    required_score_to_pass = models.IntegerField(default=50)
    quiz_for = models.ManyToManyField(Syllabus, related_name='quizzes_for_this_syllabus')
    is_randomized = models.BooleanField(default=False)
    quiz_session = models.ForeignKey(QuizSession, on_delete=models.CASCADE, related_name='quizzes', null=True, blank=True)
    status = models.SmallIntegerField(choices=QuizStatus.choices, default=QuizStatus.DRAFT)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    objects = QuizQuerySet.as_manager()

    class Meta:
        verbose_name = "Quiz"
        verbose_name_plural = "Quizzes"
    

    def can_publish(self):
        # Check if the quiz can be published
        return self.status == QuizStatus.DRAFT and self.quiz_for.exists()
    
    def __str__(self):
        return self.title or "Untitled Quiz"


