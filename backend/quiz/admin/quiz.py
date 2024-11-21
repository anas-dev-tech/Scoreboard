from django.contrib import admin
from django.urls import path
from django.shortcuts import render, redirect
from django.contrib import messages
from icecream import ic
from ..models import Quiz, QuestionOption
from academics.models import CourseAssignment
from ..forms import QuestionForm



@admin.register(Quiz)
class QuizAdmin(admin.ModelAdmin):
    """Admin View for Quiz"""

    list_display = ("title", "time", 'status')
    list_filter = ("course_assignments__course", 'status', 'course_assignments__student_group', 'course_assignments__teacher')
