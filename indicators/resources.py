from datetime import datetime

from import_export import resources, fields
from import_export.widgets import ForeignKeyWidget

from accounts.models import Teacher
from commons.models import University
from indicators.models import Indicator, SubjectData, Level
from subjects.models import PrimarySubject, SecondarySubject


class LevelResource(resources.ModelResource):
    class Meta:
        model = Level


class IndicatorResource(resources.ModelResource):
    class Meta:
        model = Indicator
        import_id_fields = ("code",)


class SubjectDataResource(resources.ModelResource):
    name = fields.Field(attribute="name", column_name="数据名称")
    # indicator = fields.Field(attribute="indicator", column_name="归属指标")
    year = fields.Field(attribute="year", column_name="归属年份")
    university = fields.Field(
        attribute="university",
        widget=ForeignKeyWidget(University, field="name"),
        column_name="归属学校",
    )
    primary_subject = fields.Field(
        attribute="primary_subject",
        widget=ForeignKeyWidget(PrimarySubject, field="name"),
        column_name="归属一级学科",
    )
    secondary_subject = fields.Field(
        attribute="secondary_subject",
        widget=ForeignKeyWidget(SecondarySubject, field="name"),
        column_name="归属二级学科",
    )
    level = fields.Field(
        attribute="level",
        widget=ForeignKeyWidget(Level, field="name"),
        column_name="归属级别",
    )
    teacher = fields.Field(
        attribute="teacher",
        widget=ForeignKeyWidget(Teacher, field="name"),
        column_name="负责人",
    )
    value = fields.Field(attribute="value")

    def __init__(self, **kwargs):
        super().__init__()
        self.user = kwargs["user"]
        self.value_fields = []

    def before_import(self, dataset, **kwargs):
        column_names = dataset.headers
        field_names = [field.column_name for field in self.get_fields()]
        self.value_fields = list(set(column_names) - set(field_names))

        dataset.headers.append("value")

        super().before_import(dataset, **kwargs)

    def before_import_row(self, row, **kwargs):
        row["value"] = {field: row[field] for field in self.value_fields}

    def before_save_instance(self, instance, row, **kwargs):
        instance.creator = self.user
        instance.updator = self.user
        instance.create_time = datetime.now()
        instance.update_time = datetime.now()

    def after_init_instance(self, instance, new, row, **kwargs):
        if "indicator" in kwargs:
            instance.indicator = kwargs["indicator"]

        if "university" in kwargs:
            instance.university = kwargs["university"]

    class Meta:
        model = SubjectData
        fields = (
            "id",
            "name",
            "year",
            "university",
            "primary_subject",
            "secondary_subject",
            "level",
            "teacher",
            "value",
        )
        import_id_fields = ("id",)
