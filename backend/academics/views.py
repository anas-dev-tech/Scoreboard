from django.shortcuts import render, get_object_or_404, get_list_or_404
from django.views.generic import TemplateView
from .models import CourseAssignment, Course
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from icecream import ic
from .forms import GradeDetailFormSet
from django.contrib.auth.mixins import LoginRequiredMixin
from users.models import Student
from core.constants import AcademicYearStatus
from django.contrib import messages


class course_assignmentTemplate(
    LoginRequiredMixin,
    TemplateView,
):
    template_name = "academics/main.html"

def main_course_assignment_detail(request):
    teacher = request.user.teacher 
    course_assignment_detail = get_list_or_404(
        CourseAssignment, teacher=teacher
    )
    total_students = course_assignment_detail.student_group.students.count()
    stu = Student.objects.filter()
    course_quiz = course_assignment_detail.quizzes.first() or "Not Set"
    context = {
        "course_assignment": course_assignment_detail,
        "total_students": total_students,
        "course_quiz": course_quiz,
    }
    
    # Check if the request is made via HTMX
    if request.htmx:
        return render(
            request, "academics/partials/course_assignment/detail.html", context
        )

    return render(request, "academics/course_assignment/detail.html", context)
    

def course_assignment_detail(request, course_assignment_id):
    course_assignment_detail = get_object_or_404(
        CourseAssignment, id=course_assignment_id
    )
    total_students = course_assignment_detail.student_group.students.count()
    course_quiz = course_assignment_detail.quizzes.first() or "Not Ready"
    context = {
        "course_assignment": course_assignment_detail,
        "total_students": total_students,
        "course_quiz": course_quiz,
    }
    # Check if the request is made via HTMX
    if request.htmx:
        ic("it is htmx")
        return render(
            request, "academics/partials/course_assignment/detail.html", context
        )
    return render(request, "academics/course_assignment/detail.html", context)



def student_list(request, course_assignment_id):
    course_assignment = get_object_or_404(CourseAssignment, id=course_assignment_id)
    students = course_assignment.student_group.students.all()

    # Pagination
    paginator = Paginator(students, 10)
    page_number = request.GET.get("page", 1)

    # return posts object as the main object
    try:
        students = paginator.page(page_number)

    except PageNotAnInteger:
        students = paginator.page(1)

    except EmptyPage:
        students = paginator.page(paginator.num_pages)

    if request.htmx:
        return render(
            request,
            "academics/partials/student/list.html",
            {
                "course_assignment": course_assignment,
                "students": students,
                "page_obj": students,
            },
        )


def student_detail(request, student_id, course_id):
    if not request.htmx:
        return

    student = get_object_or_404(Student, id=student_id)
    course = get_object_or_404(Course, id=course_id)
    student_grade = student.grades.filter(
        academic_year__status=AcademicYearStatus.CURRENT, course=course
    ).first()
    grade_details = student_grade.grade_details.all()

    if request.method == "POST":
        formset = GradeDetailFormSet(request.POST, queryset=grade_details)
        context = {
            "student": student,
            "formset": formset,
            "course_id": course_id,
        }

        if formset.is_valid():
            formset.save()
            messages.success(request, "Grade details updated successfully.")
        else:
            messages.error(request, "Error updating grade details.")

        return render(request, "academics/partials/student/detail.html", context)

    else:
        formset = GradeDetailFormSet(queryset=grade_details)
        context = {
            "student": student,
            "formset": formset,
            "course_id": course_id,
        }
        return render(request, "academics/partials/student/detail.html", context)
