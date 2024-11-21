from django.urls import path
from .  import views


app_name = 'academics'
urlpatterns = [
    path('', views.course_assignmentTemplate.as_view(), name='course_assignment'),
    path('course_assignment/<int:course_assignment_id>', views.course_assignment_detail, name='course_assignment_detail'),
    path('student/<int:student_id>/<int:course_id>', views.student_detail, name='student_detail'),
    path('course_assignment/<int:course_assignment_id>/student/', views.student_list, name='student_list')
]
