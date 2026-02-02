from django.apps import AppConfig


class ContentsConfig(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = "contents"
    verbose_name = "内容管理"
    verbose_name_plural = verbose_name
