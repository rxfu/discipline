from django.apps import AppConfig


class IndicatorsConfig(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = "indicators"
    verbose_name = "指标管理"
    verbose_name_plural = verbose_name
