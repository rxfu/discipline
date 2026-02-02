from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import TemplateView

from contents.models import News


# Create your views here.
class IntroductionView(LoginRequiredMixin, TemplateView):
    template_name = "contents/introduction.html"
    login_url = "admin/login"


class OrganizationView(LoginRequiredMixin, TemplateView):
    template_name = "contents/organization.html"
    login_url = "admin/login"


class TeamView(LoginRequiredMixin, TemplateView):
    template_name = "contents/team.html"
    login_url = "admin/login"


class NewsView(LoginRequiredMixin, TemplateView):
    template_name = "contents/news.html"
    login_url = "admin/login"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["items"] = News.objects.all()
        context["title"] = "新闻"
        return context


class DevelopmentView(LoginRequiredMixin, TemplateView):
    template_name = "contents/news.html"
    login_url = "admin/login"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["items"] = News.objects.all()
        context["title"] = "学科发展信息"
        return context


class InitiativeView(LoginRequiredMixin, TemplateView):
    template_name = "contents/news.html"
    login_url = "admin/login"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["items"] = News.objects.all()
        context["title"] = "双一流建设"
        return context


class ArticleView(LoginRequiredMixin, TemplateView):
    template_name = "contents/article.html"
    login_url = "admin/login"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["item"] = News.objects.get(pk=self.kwargs["id"])
        return context
