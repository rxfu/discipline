from django.contrib import admin
from django.http import HttpResponse
from django.urls import path


class DisciplineAdmin(admin.AdminSite):
    def get_urls(self):
        urls = super().get_urls()
        urls += [path("stats/", self.admin_view(self.statistics_View))]
        return urls

    def statistics_View(self, request):
        return HttpResponse("统计页面！")


admin_site = DisciplineAdmin(name="学科分析网站")
