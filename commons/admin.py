from django.contrib import admin
from import_export.admin import ImportExportModelAdmin

from commons.models import (
    Province,
    University,
    Department,
    Gender,
    Title,
    Education,
    Degree,
)
from commons.resources import (
    ProvinceResource,
    UniversityResource,
    DepartmentResource,
    GenderResource,
    TitleResource,
    EducationResource,
    DegreeResource,
)

admin.site.site_title = "广西学科数据分析中心"
admin.site.site_header = "广西学科数据分析中心"


# Register your models here.
@admin.register(Province)
class ProvinceAdmin(ImportExportModelAdmin):
    resource_classes = [ProvinceResource]
    list_display = ["code", "name", "short_name", "pinyin"]


@admin.register(University)
class UniversityAdmin(ImportExportModelAdmin):
    resource_classes = [UniversityResource]
    list_display = ["code", "name", "province", "description"]


@admin.register(Department)
class DepartmentAdmin(ImportExportModelAdmin):
    resource_classes = [DepartmentResource]
    list_display = ["code", "name", "university", "description"]


@admin.register(Gender)
class GenderAdmin(ImportExportModelAdmin):
    resource_classes = [GenderResource]
    list_display = ["id", "name"]


@admin.register(Title)
class TitleAdmin(ImportExportModelAdmin):
    resource_classes = [TitleResource]
    list_display = ["id", "name"]


@admin.register(Education)
class EducationAdmin(ImportExportModelAdmin):
    resource_classes = [EducationResource]
    list_display = ["id", "name"]


@admin.register(Degree)
class DegreeAdmin(ImportExportModelAdmin):
    resource_classes = [DegreeResource]
    list_display = ["id", "name"]
