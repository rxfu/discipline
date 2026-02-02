from django.db import models

from accounts.models import User


# Create your models here.
class Category(models.Model):
    name = models.CharField(max_length=100, verbose_name="分类名称")
    description = models.TextField(null=True, blank=True, verbose_name="分类描述")

    class Meta:
        verbose_name = "分类管理"
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.name


class News(models.Model):
    title = models.CharField(max_length=100, verbose_name="新闻标题")
    content = models.TextField(null=True, blank=True, verbose_name="新闻内容")
    attachment = models.FileField(null=True, blank=True, verbose_name="附件")
    category = models.ForeignKey(
        Category, on_delete=models.DO_NOTHING, verbose_name="新闻分类"
    )
    is_published = models.BooleanField(default=True, verbose_name="是否发布")
    published_time = models.DateTimeField(
        null=True, blank=True, verbose_name="发布时间"
    )
    is_top = models.BooleanField(default=False, verbose_name="是否置顶")
    creator = models.ForeignKey(
        User,
        on_delete=models.DO_NOTHING,
        related_name="created_news",
        verbose_name="创建者",
    )
    updator = models.ForeignKey(
        User,
        on_delete=models.DO_NOTHING,
        related_name="updated_news",
        verbose_name="更新者",
    )
    created_time = models.DateTimeField(auto_now_add=True, verbose_name="创建时间")
    updated_time = models.DateTimeField(auto_now=True, verbose_name="修改时间")

    class Meta:
        verbose_name = "新闻管理"
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.title


class Message(models.Model):
    title = models.CharField(max_length=100, verbose_name="消息标题")
    content = models.TextField(null=True, blank=True, verbose_name="消息内容")
    sender = models.ForeignKey(
        User,
        on_delete=models.DO_NOTHING,
        related_name="sent_messages",
        verbose_name="发送者",
    )
    recipient = models.ForeignKey(
        User,
        on_delete=models.DO_NOTHING,
        related_name="received_messages",
        verbose_name="接收者",
    )
    sent_time = models.DateTimeField(auto_now_add=True, verbose_name="发送时间")

    class Meta:
        verbose_name = "消息管理"
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.title
