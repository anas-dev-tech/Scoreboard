from django.urls import path
from . import views

app_name = 'quiz'

urlpatterns = [
    path('', views.QuizTeacherListView.as_view(), name='teacher_quiz_list'),
    path('update/<int:quiz_id>/', views.quiz_teacher_update_view, name='teacher_quiz_update'),
    path('<int:quiz_id>/question/create/', views.create_question, name='create-question'),
    path('<int:quiz_id>/question/', views.question_list, name='list-question'),
    path('<int:quiz_id>/question/<question_id>/update', views.edit_question, name="edit-question")
]
