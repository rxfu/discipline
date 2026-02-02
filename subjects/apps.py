from django.apps import AppConfig


class SubjectsConfig(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = "subjects"
    verbose_name = "学科管理"
    verbose_name_plural = verbose_name
