from django.contrib import admin
from django.contrib.admin import display
from django.db.models import JSONField
from django.urls import path
from django.utils.html import format_html
from django.utils.safestring import mark_safe
from django_json_widget.widgets import JSONEditorWidget
from import_export.admin import ImportExportModelAdmin

from indicators.forms import SubjectDataImportForm, SubjectDataConfirmImportForm
from indicators.models import Indicator, SubjectData, Level
from indicators.resources import LevelResource, IndicatorResource, SubjectDataResource
from indicators.views import (
    DataSearchView,
    PivotTableView,
    ChartView,
    LineView,
    RankView,
    BarView,
    QuadrantView,
)


# Register your models here.
@admin.register(Level)
class LevelAdmin(ImportExportModelAdmin):
    resource_classes = [LevelResource]
    list_display = ["name", "weight", "remark"]


@admin.register(Indicator)
class IndicatorAdmin(ImportExportModelAdmin):
    resource_classes = [IndicatorResource]
    list_display = ["code", "name", "weight", "parent", "is_enable", "description"]

    def get_urls(self):
        return [
            path(
                "<str:code>/search",
                self.admin_site.admin_view(DataSearchView.as_view()),
                name="data_search",
            ),
            *super().get_urls(),
        ]


@admin.register(SubjectData)
class SubjectDataAdmin(ImportExportModelAdmin):
    resource_classes = [SubjectDataResource]
    import_form_class = SubjectDataImportForm
    confirm_form_class = SubjectDataConfirmImportForm
    list_display = [
        "id",
        "name",
        "get_value",
        "indicator",
        "year",
        "university",
        "primary_subject",
        "secondary_subject",
        "level",
        "teacher",
        "remark",
    ]
    fields = [
        "name",
        "value",
        "indicator",
        "year",
        "university",
        "primary_subject",
        "secondary_subject",
        "level",
        "teacher",
        "remark",
    ]

    formfield_overrides = {
        JSONField: {"widget": JSONEditorWidget},
    }

    @display(description="数据内容")
    def get_value(self, obj):
        data = (
            [
                format_html(
                    "<li style='display:inline-block; padding-right: 20px'><strong>{}：</strong>{}</li>",
                    key,
                    value,
                )
                for key, value in obj.value.items()
            ]
            if obj.value is not None
            else "无"
        )

        return mark_safe("<ul style='list-style:none'>" + "".join(data) + "</ul>")

    def get_import_resource_kwargs(self, request, **kwargs):
        kwargs = super().get_import_resource_kwargs(request, **kwargs)
        kwargs.update({"user": request.user})
        return kwargs

    def get_confirm_form_initial(self, request, import_form):
        initial = super().get_confirm_form_initial(request, import_form)

        if import_form:
            initial["indicator"] = import_form.cleaned_data["indicator"].code
            initial["university"] = import_form.cleaned_data["university"].code
        return initial

    def get_import_data_kwargs(self, request, *args, **kwargs):
        """
        Prepare kwargs for import_data.
        """
        form = kwargs.get("form", None)
        if form and hasattr(form, "cleaned_data"):
            kwargs.update({"indicator": form.cleaned_data.get("indicator", None)})
            kwargs.update({"university": form.cleaned_data.get("university", None)})
        return kwargs

    def get_urls(self):
        return [
            path(
                "pivot/",
                self.admin_site.admin_view(PivotTableView.as_view()),
                name="data_pivot",
            ),
            path(
                "chart/",
                self.admin_site.admin_view(ChartView.as_view()),
                name="data_chart",
            ),
            path(
                "bar/",
                self.admin_site.admin_view(BarView.as_view()),
                name="data_bar",
            ),
            path(
                "trend/",
                self.admin_site.admin_view(LineView.as_view()),
                name="data_line",
            ),
            path(
                "rank/",
                self.admin_site.admin_view(RankView.as_view()),
                name="data_rank",
            ),
            path(
                "quadrant/",
                self.admin_site.admin_view(QuadrantView.as_view()),
                name="data_quadrant",
            ),
            *super().get_urls(),
        ]
