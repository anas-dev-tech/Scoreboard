from typing import Any
from django.contrib import admin
from django.db.models.query import QuerySet
from django.urls import path
from django.contrib import messages
from django.shortcuts import redirect
from users.models import StudentGroup, Student
from quiz.models import Quiz
from .models import AcademicYear, Major, Course, CourseAssignment, GradeType, Grade, GradeDetail
from core.constants import YearLevel, AcademicYearStatus
from icecream import ic
from django.forms.models import BaseInlineFormSet
from django.core.exceptions import ValidationError
from django.db.models import Sum
from core.constants import GradeStatus
from .services import aggregate_course_grades



@admin.register(AcademicYear)
class AcademicYearAdmin(admin.ModelAdmin):
    list_display = ("start_year", "end_year", "status", "current_semester")
    change_list_template = "admin/academics/academic_year/change_list.html"
    # exclude = ['status',]
    def finish_current_year_view(self, request):
        # Only fetch the current year instance to finish
        try:
            AcademicYear.objects.start_upcoming_year()
            messages.success(request, "Current year finished successfully.")
        except Exception as e:
            messages.error(request, f"Error starting upcoming year: {e}")

        return redirect("..")

    def get_urls(self):
        urls = super().get_urls()
        custom_urls = [
            path(
                "finish-year/",
                self.admin_site.admin_view(self.finish_current_year_view),
                name="finish_current_year",
            ),
        ]
        return custom_urls + urls


@admin.register(Major)
class MajorAdmin(admin.ModelAdmin):
    list_display = ("name", "duration_years")

class CourseAssignmentInline(admin.TabularInline):
    model = CourseAssignment
    extra = 1
    
    def formfield_for_foreignkey(self, db_field, request=None, **kwargs):
        if db_field.name == "student_group":
            # Check if a Course object is available in the request (this happens on edit pages)
            course = getattr(request, "_course_obj", None)
            if course:
                # Filter student groups based on the course's year_level and major
                kwargs["queryset"] = StudentGroup.objects.filter(
                    year_level=course.year_level,
                    major=course.major
                )
            else:
                # Return an empty queryset initially
                kwargs["queryset"] = StudentGroup.objects.none()
        return super().formfield_for_foreignkey(db_field, request, **kwargs)


class GradeTypeInlineModelFormSet(BaseInlineFormSet):
    def clean(self):
        super().clean()
        
        total_score = 0
        for form in self.forms:
            if not form.cleaned_data.get('DELETE', False):
                score = form.cleaned_data.get('max_score', 0)  # Assuming `score` is a field in InlineModel
                total_score += score
        
        # Access the max_score from the instance of the main model
        max_score = self.instance.max_score  # Assuming `max_score` is a field in MainModel

        if ic(total_score != max_score):
            raise ValidationError(f"The total score of all items must equal {max_score}.")


class GradeTypeInline(admin.TabularInline):
    model = GradeType
    formset = GradeTypeInlineModelFormSet
    extra = 1

    
@admin.register(Course)
class CourseAdmin(admin.ModelAdmin):
    list_display = ("name", 'major', 'year_level')
    list_filter = ['major', 'year_level']
    search_fields = ['name']
    
    actions = ['aggregate_course_result']
    inlines = [
        CourseAssignmentInline,
        GradeTypeInline,
    ]
    
    def get_form(self, request, obj=None, **kwargs):
        # Attach the current Course object to the request
        request._course_obj = obj
        return super().get_form(request, obj, **kwargs)
    
    def aggregate_course_result(self, request, queryset):
        for course in (courses:=queryset):
            aggregate_course_grades(courses=course)
            self.message_user(request, f"Aggregate course result for {course.name} completed successfully.")
            
        return redirect(".")
            
            

    aggregate_course_result.short_description = "Aggregate Course Result"

    def get_urls(self):
        urls = super().get_urls()
        custom_urls = [
            path(
                "aggregate-course-result/",
                self.admin_site.admin_view(self.aggregate_course_result),
                name="aggregate_course_result",
            ),
        ]
        return custom_urls + urls

class YearLevelFilter(admin.SimpleListFilter):
    title = "Year Level"
    parameter_name = "year_level"

    def lookups(self, request, model_admin):
        return YearLevel.choices

    def queryset(self, request: Any, queryset: QuerySet[Any]) -> QuerySet[Any] | None:
        if self.value():
            return queryset.filter(student_group__year_level=self.value())
        return queryset




@admin.register(CourseAssignment)
class CourseAssignmentAdmin(admin.ModelAdmin):
    """Admin View for Syllabus"""
    exclude = [
        "created_at",
        "updated_at",
        'deleted_at'
    ]
    list_display = (
        "student_group",
        "course",
        "teacher",
    )
    list_filter = [
        "student_group__major",
        "course",
        "student_group__year_level",
        "teacher",
    ]
    actions = ["duplicate_syllabus_for_new_year", "create_quizzes_for_syllabus"]
    list_per_page = 10



    

    def create_quizzes_for_syllabus(self, request, queryset):
        syllabuses_ids = queryset.values_list("id", flat=True)
        Quiz.objects.create_quizzes_for_syllabuses(syllabuses_ids)
        messages.success(request, "Quizzes created successfully.")
    create_quizzes_for_syllabus.short_description = (
        "Create Quizzes for Selected Syllabuses"
    )


class GradeDetailFormSet(BaseInlineFormSet):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.can_delete = False
        self.extra=0

class GradeDetailInline(admin.TabularInline):
    model = GradeDetail
    formset = GradeDetailFormSet
    readonly_fields =  ('type',)
    exclude = ('max_score',)

@admin.register(Grade)
class GradeAdmin(admin.ModelAdmin):
    list_display = ( 'student', "course","score")
    list_filter = ['course',]
    search_fields = ('student',)
    inlines = [
        GradeDetailInline,
    ]