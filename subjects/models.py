from django.db import models


# Create your models here.
class SubjectCategory(models.Model):
    code = models.CharField(max_length=2, verbose_name="门类代码", primary_key=True)
    name = models.CharField(max_length=50, verbose_name="门类名称")
    description = models.TextField(null=True, blank=True, verbose_name="门类描述")

    class Meta:
        verbose_name = "学科门类"
        verbose_name_plural = verbose_name
        ordering = ["code"]

    def __str__(self):
        return f"[{self.code}] {self.name}"


class PrimarySubject(models.Model):
    code = models.CharField(max_length=4, verbose_name="一级学科代码", primary_key=True)
    name = models.CharField(max_length=100, verbose_name="一级学科名称")
    category = models.ForeignKey(
        SubjectCategory,
        on_delete=models.CASCADE,
        related_name="primary_subjects",
        verbose_name="所属门类",
    )
    description = models.TextField(null=True, blank=True, verbose_name="一级学科描述")

    class Meta:
        verbose_name = "一级学科"
        verbose_name_plural = verbose_name
        ordering = ["category__code", "code"]

    def __str__(self):
        return f"{self.category} - [{self.code}] {self.name}"


class SecondarySubject(models.Model):
    code = models.CharField(max_length=6, verbose_name="二级学科代码", primary_key=True)
    name = models.CharField(max_length=100, verbose_name="二级学科名称")
    primary_subject = models.ForeignKey(
        PrimarySubject,
        on_delete=models.CASCADE,
        related_name="secondary_subjects",
        verbose_name="所属一级学科",
    )
    description = models.TextField(null=True, blank=True, verbose_name="二级学科描述")

    class Meta:
        verbose_name = "二级学科"
        verbose_name_plural = verbose_name
        ordering = ["primary_subject__category__code", "primary_subject__code", "code"]

    def __str__(self):
        return f"{self.primary_subject} - [{self.code}] {self.name}"
