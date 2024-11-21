from .models import AcademicYear, CourseAssignment, Grade, Course, GradeDetail, GradeType
from core.constants import AcademicYearStatus, YearLevel, GradeStatus
from users.models import StudentGroup, Student
from django.db.models.signals import pre_save, post_save
from django.dispatch import receiver
from icecream import ic
from .services import create_grade_for_assigned_course, reset_all_courses_status_to_DRAFT, upgrade_all_student_groups_year_level_by_one_year


@receiver(post_save, sender=AcademicYear)
def start_new_year(sender, instance, created, **kwargs):
    if created:
        # Upgrade the year level of the student groups
        upgrade_all_student_groups_year_level_by_one_year()

        # reset the status of the Courses to DRAFT
        reset_all_courses_status_to_DRAFT()
        
        

@receiver(pre_save, sender=AcademicYear)
def finish_current_year(sender, instance, **kwargs):
    # Check if the instance is being updated (not created)
    if instance.pk is not None:
        # Get the previous instance from the database
        previous_instance = sender.objects.get(pk=instance.pk)
        if previous_instance.status == AcademicYearStatus.CURRENT:
            if instance.status == AcademicYearStatus.FINISHED:
                syllabuses = CourseAssignment.objects.all()
                for syllabus in syllabuses:
                    syllabus.delete()



@receiver(post_save, sender=CourseAssignment)
def create_grade_when_assign_course(sender, instance, created, **kwargs):
    if created and instance.course.status == GradeStatus.PUBLISHED:
        create_grade_for_assigned_course(course_assignments=[instance])

            
@receiver(pre_save, sender=Course)
def create_course_result(sender, instance,**kwargs):
    old_instance = sender.objects.filter(pk=instance.pk).first() or None
    if old_instance is not None and old_instance.status == GradeStatus.DRAFT and instance.status == GradeStatus.PUBLISHED:
        course_assignments = instance.course_assignments.all()
        create_grade_for_assigned_course(course_assignments=course_assignments)
        
        
        
        
        
        # student_group = instance.course_assignments.all().values_list('student_group', flat=True)
        # students = Student.objects.filter(group__in=student_group)
        # grade_types =  GradeType.objects.filter(course=instance)

        # for student in students:
        #     course_result = Grade.objects.create(
        #                 student=student,
        #                 major=instance.major,
        #                 year_level=instance.year_level,
        #                 course=instance,
        #                 semester=instance.semester,
        #                 max_score=instance.max_score
        #             )
        #     for grade_type in grade_types:
        #         GradeDetail.objects.create(
        #             course_result=course_result,
        #             type=grade_type,
        #             max_score=grade_type.max_score
        #         )



