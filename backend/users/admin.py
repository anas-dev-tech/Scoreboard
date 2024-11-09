from django.contrib.auth import get_user_model
from .models import Teacher, Student, StudentGroup
import pandas as pd
from django.shortcuts import redirect
from django.urls import path, reverse
import pandas as pd
from django.contrib import admin, messages
from django.shortcuts import render, redirect
from django.urls import path
from .models import Student
from .forms import StudentImportForm
from core.utils import ImportData
from icecream import ic

User = get_user_model()


@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    """Admin View for"""

    list_display = (
        "email",
        "role",
        "is_staff",
        "is_superuser",
        "is_active",
        "last_login",
        "date_joined",
        "force_change_password",
    )
    list_filter = (
        "role",
        "is_staff",
        "is_superuser",
        "is_active",
        "last_login",
        "date_joined",
        "force_change_password",
    )
    search_fields = ("email", "first_name", "last_name")
    list_per_page = 20
    fieldsets = (
        ("Personal Info", {"fields": ("first_name", "last_name")}),
        ("Role", {"fields": ("role", "is_staff", "is_superuser")}),
        ("Credential", {"fields": ("email", "password")}),
    )

    def save_model(self, request, obj, form, change):
        password = form.cleaned_data.get("password")
        if password and not password.startswith("pbkdf2_sha256$"):
            obj.set_password(form.cleaned_data["password"])
        super().save_model(request, obj, form, change)


@admin.register(Teacher)
class TeacherAdmin(admin.ModelAdmin):
    """Admin View for Teacher)"""
    list_display = ("user",)
    list_per_page = 20


@admin.register(StudentGroup)
class StudentGroupAdmin(admin.ModelAdmin):
    """Admin View for StudentGroup)"""

    list_display = ("number", "major")
    list_filter = ["major", "year_level"]
    list_per_page = 20


@admin.register(Student)
class StudentAdmin(admin.ModelAdmin):
    list_display = ("id", "name", "group")
    list_filter = ["group"]
    list_per_page = 12
    change_list_template = "admin/student_list_buttons.html"

    def import_students_view(self, request):
        if request.method == "POST":
            form = StudentImportForm(request.POST, request.FILES)
            if form.is_valid():
                group = form.cleaned_data["group"]
                file = request.FILES["file"]

                try:
                    excel_to_model_mappings = {
                        "id": "id",
                        "name": "name",
                    }
                    student_list = ImportData(file).excel_to_model_instances(
                        Student, excel_to_model_mappings
                    )

                    for student in student_list:
                        student.group = group
                        student.save()

                    self.message_user(
                        request, "Students imported successfully.", messages.SUCCESS
                    )
                    return redirect("..")
                except Exception as e:
                    self.message_user(
                        request, f"Error importing students: {e}", messages.ERROR
                    )
                    return redirect("..")
        else:
            form = StudentImportForm()

        return render(request, "admin/import_students.html", {"form": form})

    def get_urls(self):
        urls = super().get_urls()
        custom_urls = [
            path(
                "import-students/",
                self.admin_site.admin_view(self.import_students_view),
                name="import-students",
            ),
        ]
        return custom_urls + urls

    def button_import_students(self, obj):
        return '<a class="button" href="{}">Import Students</a>'.format(
            reverse("admin:import-students")
        )
