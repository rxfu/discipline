from import_export import resources

from accounts.models import User, Teacher


class UserResource(resources.ModelResource):
    class Meta:
        model = User


class TeacherResource(resources.ModelResource):
    class Meta:
        model = Teacher
