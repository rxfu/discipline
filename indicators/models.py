from django.core.serializers.json import DjangoJSONEncoder
from django.db import models

from accounts.models import User, Teacher
from commons.models import University, PrimarySubject, SecondarySubject


# Create your models here.
class Level(models.Model):
    name = models.CharField(max_length=255, verbose_name="级别名称", unique=True)
    weight = models.FloatField(default=1.0, verbose_name="级别权重")
    remark = models.TextField(null=True, blank=True, verbose_name="备注")

    class Meta:
        verbose_name = "级别表"
        verbose_name_plural = verbose_name
        ordering = ("id",)

    def __str__(self):
        return self.name


class Indicator(models.Model):
    code = models.CharField(max_length=6, verbose_name="指标编码", primary_key=True)
    name = models.CharField(max_length=100, verbose_name="指标名称")
    weight = models.FloatField(default=1.0, verbose_name="指标权重")
    parent = models.ForeignKey(
        "self",
        null=True,
        blank=True,
        on_delete=models.CASCADE,
        related_name="children",
        verbose_name="父指标",
    )
    is_enable = models.BooleanField(default=True, verbose_name="是否启用")
    description = models.TextField(null=True, blank=True, verbose_name="指标描述")

    class Meta:
        verbose_name = "指标表"
        verbose_name_plural = verbose_name
        ordering = ("code",)

    def __str__(self):
        return (
            f"{self.parent} - [{self.code}] {self.name}"
            if self.parent
            else f"[{self.code}] {self.name}"
        )

    def get_all_children(self):
        """
        递归获取所有子指标
        :return: list
        """
        children = []
        for child in self.children.all():
            children.append(child)
            children.extend(child.get_all_children())

        return children


class SubjectData(models.Model):
    indicator = models.ForeignKey(
        Indicator,
        to_field="code",
        null=True,
        blank=True,
        on_delete=models.CASCADE,
        verbose_name="归属指标",
    )
    university = models.ForeignKey(
        University,
        to_field="code",
        null=True,
        blank=True,
        on_delete=models.CASCADE,
        verbose_name="归属学校",
    )
    primary_subject = models.ForeignKey(
        PrimarySubject,
        to_field="code",
        null=True,
        blank=True,
        on_delete=models.DO_NOTHING,
        verbose_name="归属一级学科",
    )
    secondary_subject = models.ForeignKey(
        SecondarySubject,
        to_field="code",
        null=True,
        blank=True,
        on_delete=models.DO_NOTHING,
        verbose_name="归属二级学科",
    )
    level = models.ForeignKey(
        Level,
        null=True,
        blank=True,
        on_delete=models.DO_NOTHING,
        verbose_name="归属级别",
    )
    year = models.IntegerField(verbose_name="归属年份")
    name = models.CharField(max_length=512, verbose_name="数据名称")
    teacher = models.ForeignKey(
        Teacher,
        null=True,
        blank=True,
        on_delete=models.CASCADE,
        verbose_name="主要负责人",
    )
    value = models.JSONField(
        encoder=DjangoJSONEncoder, null=True, blank=True, verbose_name="指标数据"
    )
    remark = models.TextField(null=True, blank=True, verbose_name="备注")
    authors = models.TextField(null=True, blank=True, verbose_name="参与者")
    departments = models.TextField(null=True, blank=True, verbose_name="参与者单位")
    grade = models.CharField(max_length=20, verbose_name="等级")
    creator = models.ForeignKey(
        User,
        on_delete=models.DO_NOTHING,
        related_name="created_datas",
        verbose_name="创建者",
    )
    updator = models.ForeignKey(
        User,
        on_delete=models.DO_NOTHING,
        related_name="updated_datas",
        verbose_name="更新者",
    )
    created_time = models.DateTimeField(auto_now_add=True, verbose_name="创建时间")
    updated_time = models.DateTimeField(auto_now=True, verbose_name="修改时间")

    class Meta:
        verbose_name = "学科数据表"
        verbose_name_plural = verbose_name
        ordering = ("-created_time",)

    def __str__(self):
        return self.name


class StatData(models.Model):
    name = models.CharField(max_length=512, verbose_name="项目名称")
    university = models.CharField(
        max_length=512, null=True, blank=True, verbose_name="单位名称"
    )
    level = models.CharField(
        max_length=512, null=True, blank=True, verbose_name="归属级别"
    )
    year = models.IntegerField(null=True, blank=True, verbose_name="归属年份")
    value = models.IntegerField(null=True, blank=True, verbose_name="数量值")
