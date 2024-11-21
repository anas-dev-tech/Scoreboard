from django.urls import path
from . import views

app_name = 'quiz'

urlpatterns = [
    path('quiz/<int:quiz_id>/', views.quiz_detail, name='quiz_detail'),
    path('', views.list_quiz, name='teacher_quiz_list'),
    path('update/<int:quiz_id>/', views.update_quiz, name='teacher_quiz_update'),
    path('create/', views.create_quiz, name='create-quiz'),
    path('<int:quiz_id>/question/create/', views.create_question, name='create-question'),
    path('<int:quiz_id>/question/create-ai/', views.create_question_AI, name='create-question-AI'),
    path('<int:quiz_id>/question/<question_id>/update', views.edit_question, name="edit-question"),
    path('<int:quiz_id>/question/', views.question_list, name='list-question'),
]
