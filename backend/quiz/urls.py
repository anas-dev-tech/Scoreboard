from django.urls import path
from . import views

urlpatterns = [
    path('', views.QuizTeacherListView.as_view(), name='teacher_quiz_list'),
]
