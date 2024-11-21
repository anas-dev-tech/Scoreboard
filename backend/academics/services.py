from .models import AcademicYear, Course, Grade, GradeType, GradeDetail, Course
from users.models import StudentGroup
from core.constants import AcademicYearStatus, GradeStatus, YearLevel

def create_grade_for_assigned_course(course_assignments):
    for course_assignment in course_assignments:
        course = course_assignment.course
        course_max_score = course.max_score
        semester = course.semester
        student_group = course_assignment.student_group
        students = student_group.students.all()
        major = student_group.major
        year_level = student_group.year_level
        current_academic_year = AcademicYear.objects.get(status=AcademicYearStatus.CURRENT)        

                
        grade_types =  GradeType.objects.filter(course=course)
        for student in students:
            course_result = Grade.objects.get_or_create(
                student=student,
                major=major,
                year_level=year_level,
                course=course,
                academic_year=current_academic_year,
                defaults={
                    'semester': semester,
                    'max_score': course_max_score,
                    }
                )

            for grade_type in grade_types:
                GradeDetail.objects.create(
                    course_result=course_result,
                    type=grade_type,
                    max_score=grade_type.max_score
                )
                
def reset_all_courses_status_to_DRAFT():
    all_courses = Course.objects.all()
    for course in all_courses:
            course.status = GradeStatus.DRAFT
            course.save()
            

def upgrade_all_student_groups_year_level_by_one_year():
    student_groups = StudentGroup.objects.exclude(year_level=YearLevel.GRADUATED).order_by('-year_level')
    for student_group in student_groups:
            max_year_level = student_group.major.duration_years
            if max_year_level == student_group.year_level:
                student_group.year_level = YearLevel.GRADUATED
            else:
                student_group.year_level += 1
            student_group.save()

def aggregate_course_grades(course):
    grades = Grade.objects.filter(
        course=course,
        academic_year__status=AcademicYearStatus.CURRENT
    )
    
    for grade in grades:
        # Calculate the total score for each student
        total_score = grade.grade_details.aggregate(total_score=Sum('score'))['total_score']
        # Update the total score in the CourseResult model
        grade.score = total_score
        grade.save()
    
    course.status = GradeStatus.AGGREGATED
    return course.save()
