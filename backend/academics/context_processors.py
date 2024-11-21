from .models import CourseAssignment
from core.constants import Role
from icecream import ic

def get_all_courses_assignment(request):
    if request.user.is_authenticated and request.user.role == Role.TEACHER:
        syllabuses = CourseAssignment.objects.filter(teacher=request.user.teacher)
        return {'courses_assignment':syllabuses}
    return dict()
