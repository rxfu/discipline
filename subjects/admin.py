from django.contrib import admin
from import_export.admin import ImportExportModelAdmin

from subjects.models import SubjectCategory, PrimarySubject, SecondarySubject
from subjects.resources import (
    SubjectCategoryResource,
    PrimarySubjectResource,
    SecondarySubjectResource,
)


# Register your models here.
@admin.register(SubjectCategory)
class SubjectCategoryAdmin(ImportExportModelAdmin):
    resource_classes = [SubjectCategoryResource]
    list_display = ["code", "name", "description"]


@admin.register(PrimarySubject)
class PrimarySubjectAdmin(ImportExportModelAdmin):
    resource_classes = [PrimarySubjectResource]
    list_display = ["code", "name", "category", "description"]


@admin.register(SecondarySubject)
class SecondarySubjectAdmin(ImportExportModelAdmin):
    resource_classes = [SecondarySubjectResource]
    list_display = [
        "code",
        "name",
        "primary_subject",
        "primary_subject__category",
        "description",
    ]
