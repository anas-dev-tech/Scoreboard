from django.urls import path
from . import views

app_name = 'quiz'

urlpatterns = [
    path('', views.QuizTeacherListView.as_view(), name='teacher_quiz_list'),
    path('update/<quiz_id>/', views.QuizTeacherUpdateView.as_view(), name='teacher_quiz_update'),
]
