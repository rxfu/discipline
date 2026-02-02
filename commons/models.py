from django.db import models

from subjects.models import PrimarySubject, SecondarySubject


# Create your models here.
class Province(models.Model):
    code = models.CharField(max_length=2, verbose_name="省份代码", primary_key=True)
    name = models.CharField(max_length=50, unique=True, verbose_name="省份名称")
    short_name = models.CharField(
        max_length=10, unique=True, null=True, blank=True, verbose_name="简称"
    )
    pinyin = models.CharField(
        max_length=100, unique=True, null=True, blank=True, verbose_name="拼音"
    )

    class Meta:
        verbose_name = "省份表"
        verbose_name_plural = verbose_name
        ordering = ("code",)

    def __str__(self):
        return self.name


class University(models.Model):
    code = models.CharField(max_length=10, verbose_name="学校代码", primary_key=True)
    name = models.CharField(max_length=100, verbose_name="学校名称", unique=True)
    province = models.ForeignKey(
        Province, to_field="code", on_delete=models.DO_NOTHING, verbose_name="所属省份"
    )
    description = models.TextField(null=True, blank=True, verbose_name="学校描述")

    class Meta:
        verbose_name = "学校表"
        verbose_name_plural = verbose_name
        ordering = ("code",)

    def __str__(self):
        return self.name


class Department(models.Model):
    code = models.CharField(
        max_length=10, verbose_name="二级单位代码", primary_key=True
    )
    name = models.CharField(max_length=100, verbose_name="二级单位名称", unique=True)
    university = models.ForeignKey(
        University, to_field="code", on_delete=models.CASCADE, verbose_name="所属学校"
    )
    primary_subjects = models.ManyToManyField(
        PrimarySubject, blank=True, verbose_name="拥有一级学科"
    )
    secondary_subjects = models.ManyToManyField(
        SecondarySubject, blank=True, verbose_name="拥有二级学科"
    )
    description = models.TextField(null=True, blank=True, verbose_name="二级单位描述")

    class Meta:
        verbose_name = "二级单位表"
        verbose_name_plural = verbose_name
        unique_together = ("university", "name")
        ordering = ("code",)

    def __str__(self):
        return f"{self.university.name}-{self.name}"


class Gender(models.Model):
    name = models.CharField(max_length=20, verbose_name="性别名称", unique=True)
    remark = models.TextField(null=True, blank=True, verbose_name="备注")

    class Meta:
        verbose_name = "性别表"
        verbose_name_plural = verbose_name
        ordering = ("id",)

    def __str__(self):
        return self.name


class Title(models.Model):
    name = models.CharField(max_length=20, verbose_name="职称名称", unique=True)
    remark = models.TextField(null=True, blank=True, verbose_name="备注")

    class Meta:
        verbose_name = "职称表"
        verbose_name_plural = verbose_name
        ordering = ("id",)

    def __str__(self):
        return self.name


class Education(models.Model):
    name = models.CharField(max_length=20, verbose_name="学历名称", unique=True)
    remark = models.TextField(null=True, blank=True, verbose_name="备注")

    class Meta:
        verbose_name = "学历表"
        verbose_name_plural = verbose_name
        ordering = ("id",)

    def __str__(self):
        return self.name


class Degree(models.Model):
    name = models.CharField(max_length=20, verbose_name="学位名称", unique=True)
    remark = models.TextField(null=True, blank=True, verbose_name="备注")

    class Meta:
        verbose_name = "学位表"
        verbose_name_plural = verbose_name
        ordering = ("id",)

    def __str__(self):
        return self.name
