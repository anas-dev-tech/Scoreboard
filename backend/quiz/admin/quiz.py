from django.contrib import admin
from django.urls import path
from django.shortcuts import render, redirect
from django.contrib import messages
from icecream import ic
from ..models import Quiz, QuestionOption
from academics.models import Syllabus
from ..forms import QuestionForm



@admin.register(Quiz)
class QuizAdmin(admin.ModelAdmin):
    """Admin View for Quiz"""

    list_display = ("title", "time", 'status')
    list_filter = ("quiz_for__course", 'status', 'quiz_for__student_group', 'quiz_for__teacher')
    actions = ['publish_quizzes']



    def publish_quizzes(self, request, queryset):
        quiz_ids = queryset.values_list("id", flat=True)
        try:
            Quiz.objects.publish_quizzes(queryset)
            messages.success(request, "Quizzes published successfully to teachers")
        except Exception as e:
            messages.error(request, f"Can't Publish selected quizzes: either they are already published or They are not assigned to specific syllabus")
    publish_quizzes.short_description = "Publish quizzes to teachers"
        