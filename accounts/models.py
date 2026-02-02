from django.contrib.auth.models import AbstractUser
from django.db import models

from commons.models import University, Department, Gender, Title, Education, Degree
from subjects.models import PrimarySubject, SecondarySubject


# Create your models here.
class User(AbstractUser):
    id = models.BigAutoField(verbose_name="用户ID", primary_key=True)
    full_name = models.CharField(
        max_length=100, null=True, blank=True, verbose_name="姓名"
    )
    phone = models.CharField(
        max_length=20, null=True, blank=True, verbose_name="联系电话"
    )
    university = models.ForeignKey(
        University,
        null=True,
        blank=True,
        on_delete=models.DO_NOTHING,
        verbose_name="所属学校",
    )
    department = models.ForeignKey(
        Department,
        null=True,
        blank=True,
        on_delete=models.DO_NOTHING,
        verbose_name="所属二级单位",
    )

    class Meta:
        verbose_name = "用户表"
        verbose_name_plural = verbose_name
        ordering = ("id",)

    def __str__(self):
        return self.username


class Teacher(models.Model):
    id = models.CharField(max_length=8, primary_key=True, verbose_name="教师工号")
    name = models.CharField(max_length=100, verbose_name="姓名")
    gender = models.ForeignKey(
        Gender, null=True, blank=True, on_delete=models.DO_NOTHING, verbose_name="性别"
    )
    birthday = models.DateField(null=True, blank=True, verbose_name="出生日期")
    title = models.ForeignKey(
        Title, null=True, blank=True, on_delete=models.DO_NOTHING, verbose_name="职称"
    )
    education = models.ForeignKey(
        Education,
        null=True,
        blank=True,
        on_delete=models.DO_NOTHING,
        verbose_name="学历",
    )
    degree = models.ForeignKey(
        Degree, null=True, blank=True, on_delete=models.DO_NOTHING, verbose_name="学位"
    )
    university = models.ForeignKey(
        University,
        null=True,
        blank=True,
        on_delete=models.DO_NOTHING,
        verbose_name="所属学校",
    )
    colleges = models.ManyToManyField(Department, blank=True, verbose_name="所属单位")
    primary_subjects = models.ManyToManyField(
        PrimarySubject, verbose_name="所属一级学科"
    )
    secondary_subjects = models.ManyToManyField(
        SecondarySubject, verbose_name="所属二级学科"
    )
    email = models.EmailField(
        max_length=200, null=True, blank=True, verbose_name="电子邮箱", unique=True
    )
    phone = models.CharField(
        max_length=20, null=True, blank=True, verbose_name="联系电话", unique=True
    )
    remarks = models.TextField(blank=True, null=True, verbose_name="备注")

    class Meta:
        verbose_name = "教师表"
        verbose_name_plural = verbose_name
        ordering = ("id",)

    def __str__(self):
        return self.name
