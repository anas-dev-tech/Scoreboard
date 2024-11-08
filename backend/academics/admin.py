from typing import Any
from django.contrib import admin
from django.db.models.query import QuerySet
from django.http import HttpResponseRedirect
from django.urls import path
from django.shortcuts import render
from django.contrib import messages
from django.shortcuts import redirect
from users.models import StudentGroup
from quiz.models import Quiz
from .models import AcademicYear, Major, Course, Syllabus
from core.constants import YearLevel
from icecream import ic


@admin.register(AcademicYear)
class AcademicYearAdmin(admin.ModelAdmin):
    list_display = ("start_year", "end_year", "status", "current_semester")
    change_list_template = "admin/academics/academic_year/change_list.html"

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


@admin.register(Course)
class CourseAdmin(admin.ModelAdmin):
    list_display = ("name",)


class YearLevelFilter(admin.SimpleListFilter):
    title = "Year Level"
    parameter_name = "year_level"

    def lookups(self, request, model_admin):
        return YearLevel.choices

    def queryset(self, request: Any, queryset: QuerySet[Any]) -> QuerySet[Any] | None:
        if self.value():
            return queryset.filter(student_group__year_level=self.value())
        return queryset


@admin.register(Syllabus)
class SyllabusAdmin(admin.ModelAdmin):
    """Admin View for Syllabus"""

    list_display = (
        "student_group",
        "course",
        "teacher",
        "academic_year",
        "semester",
    )
    list_filter = [
        "student_group__major",
        "course",
        "student_group__year_level",
        "academic_year",
        "teacher",
    ]
    actions = ["duplicate_syllabus_for_new_year", "create_quizzes_for_syllabus"]
    list_per_page = 10

    def get_changelist_instance(self, request):
        # Modify request.GET to set a default filter value
        if "academic_year__id__exact" not in request.GET:
            # Set the default filter to a specific category ID, e.g., category id 1
            default_filters = {
                "academic_year__id__exact": str(
                    ic(AcademicYear.objects.get_current_year().id)
                )
            }
            request.GET = request.GET.copy()
            request.GET.update(default_filters)

        return super().get_changelist_instance(request)

    def duplicate_syllabus_for_new_year(self, request, queryset):

        for syllabus in queryset:
            Syllabus.objects.copy_syllabus_to_current_year(syllabus.id)

        self.message_user(request, "Syllabus duplicated for the new year.")
        return HttpResponseRedirect(request.get_full_path())

    duplicate_syllabus_for_new_year.short_description = (
        "Duplicate Syllabus for New Year"
    )

    def create_quizzes_for_syllabus(self, request, queryset):
        syllabuses_ids = queryset.values_list("id", flat=True)
        Quiz.objects.create_quizzes_for_syllabuses(syllabuses_ids)
        messages.success(request, "Quizzes created successfully.")
    create_quizzes_for_syllabus.short_description = (
        "Create Quizzes for Selected Syllabuses"
    )
    
    