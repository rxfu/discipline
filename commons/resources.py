from import_export import resources

from commons.models import (
    Province,
    University,
    Department,
    Gender,
    Title,
    Education,
    Degree,
)


class ProvinceResource(resources.ModelResource):
    class Meta:
        model = Province
        import_id_fields = ("code",)


class UniversityResource(resources.ModelResource):
    class Meta:
        model = University


class DepartmentResource(resources.ModelResource):
    class Meta:
        model = Department
        import_id_fields = ("code",)


class GenderResource(resources.ModelResource):
    class Meta:
        model = Gender


class TitleResource(resources.ModelResource):
    class Meta:
        model = Title


class EducationResource(resources.ModelResource):
    class Meta:
        model = Education


class DegreeResource(resources.ModelResource):
    class Meta:
        model = Degree
