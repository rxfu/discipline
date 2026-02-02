from django.contrib import admin
from django.contrib.admin import display
from django.contrib.auth.admin import UserAdmin
from import_export.admin import ImportExportModelAdmin

from accounts.models import User, Teacher
from accounts.resources import UserResource, TeacherResource


# Register your models here.
@admin.register(User)
class UserAdmin(UserAdmin, ImportExportModelAdmin):
    resource_classes = [UserResource]
    list_display = (
        "username",
        "full_name",
        "phone",
        "email",
        "university",
        "department",
        "is_staff",
        "is_active",
    )


@admin.register(Teacher)
class TeacherAdmin(ImportExportModelAdmin):
    resource_classes = [TeacherResource]
    list_display = (
        "id",
        "name",
        "title",
        "education",
        "degree",
        "university",
        "get_colleges",
        "get_primary_subject",
        "get_secondary_subject",
        "remarks",
    )

    @display(description="所属学院")
    def get_colleges(self, obj):
        return "、".join([college.name for college in obj.colleges.all()])

    @display(description="所属一级学科")
    def get_primary_subject(self, obj):
        return "、".join([subject.name for subject in obj.primary_subjects.all()])

    @display(description="所属二级学科")
    def get_secondary_subject(self, obj):
        return "、".join([subject.name for subject in obj.secondary_subjects.all()])
