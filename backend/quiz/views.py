from django.shortcuts import render
from django.views.generic import ListView
from .models import Quiz
from django.contrib.auth.mixins import LoginRequiredMixin
class TeacherUserMixin:
    def get_teacher(self):
        user = self.request.user
        return user.teacher if hasattr(user, 'teacher') and user.is_teacher else None


class QuizTeacherMixin(TeacherUserMixin):
    model = Quiz
    
    def get_queryset(self):
        teacher = self.get_teacher()
        
        if teacher:
            queryset = super().get_queryset()
            return queryset.get_quizzes_for_teacher(teacher.id)
        
        return self.model.objects.none()


class QuizTeacherListView(LoginRequiredMixin, QuizTeacherMixin, ListView):
    model = Quiz
    template_name = 'quiz/teacher/list.html'
    context_object_name = 'quizzes'
