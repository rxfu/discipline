from django.contrib import admin
from django.urls import path

from contents.models import Category, Message, News
from contents.views import (
    IntroductionView,
    NewsView,
    OrganizationView,
    TeamView,
    DevelopmentView,
    InitiativeView,
    ArticleView,
)


# Register your models here.
@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ["name", "description"]


@admin.register(News)
class NewsAdmin(admin.ModelAdmin):
    list_display = ["title", "category", "is_published", "is_top", "published_time"]

    def get_urls(self):
        return [
            path(
                "introduction/",
                self.admin_site.admin_view(IntroductionView.as_view()),
                name="introduction",
            ),
            path(
                "organization/",
                self.admin_site.admin_view(OrganizationView.as_view()),
                name="organization",
            ),
            path(
                "team/",
                self.admin_site.admin_view(TeamView.as_view()),
                name="team",
            ),
            path(
                "news/",
                self.admin_site.admin_view(NewsView.as_view()),
                name="news",
            ),
            path(
                "development/",
                self.admin_site.admin_view(DevelopmentView.as_view()),
                name="development",
            ),
            path(
                "initiative/",
                self.admin_site.admin_view(InitiativeView.as_view()),
                name="initiative",
            ),
            path(
                "<int:id>/article/",
                self.admin_site.admin_view(ArticleView.as_view()),
                name="article",
            ),
            *super().get_urls(),
        ]


@admin.register(Message)
class MessageAdmin(admin.ModelAdmin):
    pass
