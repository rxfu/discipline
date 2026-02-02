from django.apps import AppConfig


class CommonsConfig(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = "commons"
    verbose_name = "基础数据管理"
    verbose_name_plural = verbose_name
