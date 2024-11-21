from django.db.models.signals import m2m_changed
from django.dispatch import receiver
from .models import Quiz
from academics.models import CourseAssignment
from django.core.exceptions import ValidationError

# @receiver(m2m_changed, sender=Quiz.quiz_for.through)
# def validate_quiz_count(sender, instance, action, reverse, pk_set, **kwargs):
#     # Only check when a new quiz is being added to a syllabus
#     if action == 'pre_add':
#         for syllabus_id in pk_set:
#             syllabus = Syllabus.objects.get(pk=syllabus_id)
#             if syllabus.quizzes_for_this_syllabus.count() >= syllabus.quiz_count:
#                 raise ValidationError(
#                     f"Cannot add more quizzes to syllabus '{syllabus}'. Maximum allowed is {syllabus.quiz_count}."
#                 )