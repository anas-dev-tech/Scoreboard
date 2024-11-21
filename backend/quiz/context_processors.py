from .models import Quiz
from core.constants import Role

def get_all_quizzes(request):
    user = request.user
    if user.is_authenticated and user.role == Role.TEACHER:
        quizzes = Quiz.objects.filter(
            course_assignments__teacher=user.teacher,

        )
        return {'quizzes': quizzes}
    return {}
    