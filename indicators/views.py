import json
from datetime import datetime

from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
from django.db.models import Count, Q
from django.views.generic import TemplateView

from indicators.models import SubjectData, Indicator, Level
from subjects.models import PrimarySubject, SecondarySubject


# Create your views here.
class DataSearchView(LoginRequiredMixin, TemplateView):
    template_name = "indicators/subjectdata.html"
    login_url = "admin:login"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        # 获取所有分类用于筛选
        indicator = Indicator.objects.get(pk=self.kwargs["code"])
        context["indicators"] = indicator.get_all_children()
        context["primary_subjects"] = PrimarySubject.objects.all()
        context["secondary_subjects"] = SecondarySubject.objects.all()
        context["levels"] = Level.objects.all()
        context["years"] = (
            SubjectData.objects.values("year").distinct().order_by("-year")
        )

        # 获取搜索参数
        search_query = self.request.GET.get("q", "")
        indicator_id = self.request.GET.get("indicator", "")
        primary_subject_id = self.request.GET.get("primary_subject", "")
        secondary_subject_id = self.request.GET.get("secondary_subject", "")
        level_id = self.request.GET.get("level", "")
        year = self.request.GET.get("year", "")

        # 构建查询结果
        ind_ids = [ind.code for ind in context["indicators"]]
        ind_ids.append(indicator.code)
        data = SubjectData.objects.select_related(
            "indicator", "primary_subject", "secondary_subject"
        ).filter(indicator_id__in=ind_ids)

        if year:
            data = data.filter(year__icontains=year)

        # 应用搜索条件
        if search_query:
            data = data.filter(name__icontains=search_query)

        # 应用筛选
        if indicator_id:
            data = data.filter(indicator_id=indicator_id)

        if primary_subject_id:
            data = data.filter(primary_subject_id=primary_subject_id)

        if secondary_subject_id:
            data = data.filter(secondary_subject_id=secondary_subject_id)

        if level_id:
            data = data.filter(level_id=level_id)

        indicator_counts = data.values("indicator__name").annotate(
            indicator_count=Count("id")
        )
        primary_subject_counts = data.values("primary_subject__name").annotate(
            primary_subject_count=Count("id")
        )
        secondary_subject_counts = data.values("secondary_subject__name").annotate(
            secondary_subject_count=Count("id")
        )
        level_counts = data.values("level__name").annotate(level_count=Count("id"))
        year_counts = (
            data.values("year").annotate(year_count=Count("year")).order_by("-year")
        )

        # 获取每页显示记录数参数，默认为10
        per_page = self.request.GET.get("per_page", 10)
        try:
            per_page = int(per_page)
            # 限制每页记录数在合理范围内
            per_page = max(5, min(per_page, 100))
        except (ValueError, TypeError):
            per_page = 10

        # 创建分页器对象
        paginator = Paginator(data, per_page)

        # 获取当前页码
        page_number = self.request.GET.get("page")

        try:
            # 获取当前页的数据
            page_data = paginator.get_page(page_number)
        except PageNotAnInteger:
            # 如果页码不是整数，返回第一页
            page_data = paginator.page(1)
        except EmptyPage:
            # 如果页码超出范围，返回最后一页
            page_data = paginator.page(paginator.num_pages)

        context["page_data"] = page_data
        context["per_page_options"] = [5, 10, 20, 50]
        context["current_per_page"] = per_page

        context["data"] = data
        context["search_query"] = search_query
        context["selected_indicator"] = indicator_id
        context["selected_primary_subject"] = primary_subject_id
        context["selected_secondary_subject"] = secondary_subject_id
        context["selected_level"] = level_id
        context["selected_year"] = year

        context["indicator_counts"] = indicator_counts
        context["primary_subject_counts"] = primary_subject_counts
        context["secondary_subject_counts"] = secondary_subject_counts
        context["level_counts"] = level_counts
        context["year_counts"] = year_counts

        context["title"] = indicator.name

        return context


class PivotTableView(LoginRequiredMixin, TemplateView):
    template_name = "indicators/pivot.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        # 获取所有字段选项
        context["row_fields"] = [
            ("indicator", "归属指标"),
            ("primary_subject", "归属一级学科"),
            ("secondary_subject", "归属二级学科"),
            ("level", "归属级别"),
            ("year", "归属年份"),
            ("teacher", "主要负责人"),
        ]
        context["col_fields"] = [
            ("indicator", "归属指标"),
            ("primary_subject", "归属一级学科"),
            ("secondary_subject", "归属二级学科"),
            ("level", "归属级别"),
            ("year", "归属年份"),
            ("teacher", "主要负责人"),
        ]
        context["title"] = "数据透视表"

        # 获取请求参数
        row_field = self.request.GET.get("row_field", "indicator")
        col_field = self.request.GET.get("col_field", "year")

        context["selected_row_field"] = row_field
        context["selected_col_field"] = col_field

        # 计算透视表数据
        pivot_data = self.calculate_pivot_data(row_field, col_field)
        context["pivot_data"] = pivot_data

        return context

    def calculate_pivot_data(self, row_field, col_field):
        # 获取所有数据
        data = SubjectData.objects.all()

        # 获取行标签和列标签的唯一值
        if row_field == "indicator":
            row_labels = list(Indicator.objects.values_list("name", flat=True))
        elif row_field == "level":
            row_labels = list(Level.objects.values_list("name", flat=True))
        else:
            row_labels = list(
                data.values_list(row_field, flat=True).order_by(col_field).distinct()
            )

        if col_field == "indicator":
            col_labels = list(Indicator.objects.values_list("name", flat=True))
        elif col_field == "level":
            col_labels = list(Level.objects.values_list("name", flat=True))
        else:
            col_labels = list(
                data.values_list(col_field, flat=True).order_by(col_field).distinct()
            )

        # 初始化透视表数据
        pivot_table = {
            "row_labels": row_labels,
            "col_labels": col_labels,
            "data": {},
            "row_totals": {},
            "col_totals": {},
            "grand_total": 0,
        }

        # 计算每个单元格的计数
        for d in data:
            # 获取行值和列值
            if row_field == "indicator":
                row_value = d.indicator.name if d.indicator else "未知"
            elif row_field == "level":
                row_value = d.level.name if d.level else "未知"
            else:
                row_value = getattr(d, row_field)

            if col_field == "indicator":
                col_value = d.indicator.name if d.indicator else "未知"
            elif col_field == "level":
                col_value = d.level.name if d.level else "未知"
            else:
                col_value = getattr(d, col_field)

            # 初始化字典
            if row_value not in pivot_table["data"]:
                pivot_table["data"][row_value] = {}
            if col_value not in pivot_table["data"][row_value]:
                pivot_table["data"][row_value][col_value] = 0

            # 增加计数
            pivot_table["data"][row_value][col_value] += 1

            # 计算行总计
            if row_value not in pivot_table["row_totals"]:
                pivot_table["row_totals"][row_value] = 0
            pivot_table["row_totals"][row_value] += 1

            # 计算列总计
            if col_value not in pivot_table["col_totals"]:
                pivot_table["col_totals"][col_value] = 0
            pivot_table["col_totals"][col_value] += 1

            # 计算总计
            pivot_table["grand_total"] += 1

        return pivot_table


class ChartView(LoginRequiredMixin, TemplateView):
    template_name = "indicators/chart.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        # 获取请求参数
        subject = self.request.GET.get("subject")
        context["selected_subject"] = subject

        data = (
            SubjectData.objects.values("year")
            .filter(primary_subject_id=subject)
            .annotate(count=Count("id"))
            .order_by("year")
        )

        subjects = PrimarySubject.objects.all()
        years = [item["year"] for item in data]
        counts = [item["count"] for item in data]

        context["subjects"] = subjects
        context["years"] = years
        context["counts"] = counts
        context["title"] = "按年份统计"

        return context


class BarView(LoginRequiredMixin, TemplateView):
    template_name = "indicators/bar.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        # 获取请求参数
        subject = self.request.GET.get("subject")
        context["selected_subject"] = subject

        parent_indicators = Indicator.objects.filter(parent_id__isnull=True)
        data_stats = {}

        for parent in parent_indicators:
            all_related_indicators = Indicator.objects.filter(
                Q(code=parent.code) | Q(parent_id=parent.code)
            )

            data = (
                SubjectData.objects.values("year")
                .filter(primary_subject_id=subject)
                .filter(indicator_id__in=all_related_indicators)
                .annotate(count=Count("id"))
                .order_by("year")
                .order_by("indicator_id")
            )

            data_stats[parent.code] = {item["year"]: item["count"] for item in data}

        subjects = PrimarySubject.objects.all()
        years = sorted(
            set(
                SubjectData.objects.values_list("year", flat=True).filter(
                    primary_subject_id=subject
                )
            )
        )
        # counts = [item["count"] for item in data]

        # 准备图表数据
        chart_data = {"labels": list(years), "datasets": []}

        # 为每个学科准备5个指标的数据
        metrics = {
            "101000": {
                "name": "人才培养",
                "color": "rgba(255, 99, 132, 1)",
                "bg_color": "rgba(255, 99, 132, 0.2)",
            },
            "102000": {
                "name": "平台项目",
                "color": "rgba(54, 162, 235, 1)",
                "bg_color": "rgba(54, 162, 235, 0.2)",
            },
            "103000": {
                "name": "成果获奖",
                "color": "rgba(255, 205, 86, 1)",
                "bg_color": "rgba(255, 205, 86, 0.2)",
            },
            "104000": {
                "name": "学术论文",
                "color": "rgba(75, 192, 192, 1)",
                "bg_color": "rgba(75, 192, 192, 0.2)",
            },
            "105000": {
                "name": "高端人才",
                "color": "rgba(153, 102, 255, 1)",
                "bg_color": "rgba(153, 102, 255, 0.2)",
            },
        }

        for code, metric in metrics.items():
            data_values = []

            for year in years:
                value = 0

                if code in data_stats and year in data_stats[code]:
                    value = data_stats[code][year]

                data_values.append(value)

            dataset = {
                "label": f"{metric['name']}",
                "data": data_values,
                "backgroundColor": metric["bg_color"],
                "borderColor": metric["color"],
                "borderWidth": 1,
            }

            chart_data["datasets"].append(dataset)

        context["chart_data"] = json.dumps(chart_data)
        context["subjects"] = subjects
        # context["years"] = years
        # context["metrics"] = metrics
        # context["counts"] = counts
        context["title"] = "按学科分析"

        return context


class LineView(LoginRequiredMixin, TemplateView):
    template_name = "indicators/line.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        data = (
            SubjectData.objects.select_related("primary_subject")
            .values("primary_subject_id", "year")
            .annotate(count=Count("id"))
            .order_by("year")
        )

        # 构建图表数据结构
        chart_data = {"labels": [], "datasets": []}  # 年份标签  # 数据集

        # 收集所有年份
        years = data.order_by("year").values_list("year", flat=True).distinct()
        chart_data["labels"] = list(years)

        # 获取所有学科
        subjects = (
            data.order_by("primary_subject_id")
            .values_list("primary_subject_id", flat=True)
            .distinct()
        )

        # 为每个学科创建数据集
        for subject_id in subjects:
            if subject_id is not None:
                # 获取该学科在各年份的数据
                subject_data = data.filter(primary_subject_id=subject_id)

                # 构建该学科的数据
                subject_values = []
                for year in years:
                    count = subject_data.filter(year=year).aggregate(count=Count("id"))[
                        "count"
                    ]
                    subject_values.append(count)

                # 获取学科名称（假设有一个方法获取名称）
                subject_name = self.get_subject_name(subject_id)  # 需要实现此函数

                dataset = {
                    "label": subject_name,
                    "data": subject_values,
                    "borderColor": self.get_color_for_subject(
                        subject_id
                    ),  # 需要实现颜色分配
                    "backgroundColor": self.get_background_color_for_subject(
                        subject_id
                    ),
                    "fill": False,
                    "tension": 0.1,
                }

                chart_data["datasets"].append(dataset)

        context["chart_data"] = json.dumps(chart_data, ensure_ascii=False)
        context["title"] = "学科趋势分析"

        return context

    def get_subject_name(self, subject_id):
        """获取学科名称的辅助函数"""
        try:
            subject = PrimarySubject.objects.get(code=subject_id)

            return subject.name
        except PrimarySubject.DoesNotExist:
            return f"学科{subject_id}"

    def get_color_for_subject(self, subject_id):
        """为不同学科分配不同颜色"""
        colors = [
            "rgba(255, 99, 132, 1)",
            "rgba(54, 162, 235, 1)",
            "rgba(255, 205, 86, 1)",
            "rgba(75, 192, 192, 1)",
            "rgba(153, 102, 255, 1)",
            "rgba(255, 159, 64, 1)",
            "rgba(199, 199, 199, 1)",
            "rgba(83, 102, 255, 1)",
        ]

        return colors[int(subject_id) % len(colors)]

    def get_background_color_for_subject(self, subject_id):
        """为不同学科分配背景颜色"""
        colors = [
            "rgba(255, 99, 132, 0.2)",
            "rgba(54, 162, 235, 0.2)",
            "rgba(255, 205, 86, 0.2)",
            "rgba(75, 192, 192, 0.2)",
            "rgba(153, 102, 255, 0.2)",
            "rgba(255, 159, 64, 0.2)",
            "rgba(199, 199, 199, 0.2)",
            "rgba(83, 102, 255, 0.2)",
        ]

        return colors[int(subject_id) % len(colors)]


class RankView(LoginRequiredMixin, TemplateView):
    template_name = "indicators/rank.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        # 获取所有学科数据，按学科和年份分组统计发文数量
        subject_data = (
            SubjectData.objects.values("primary_subject__name", "year")
            .annotate(count=Count("id"))
            .order_by("primary_subject__name", "year")
        )

        # 构建学科年度数据字典
        subject_year_data = {}
        all_years = set()

        for item in subject_data:
            subject_name = item["primary_subject__name"]

            if subject_name is not None:
                year = item["year"]
                count = item["count"]

                if subject_name not in subject_year_data:
                    subject_year_data[subject_name] = {}

                subject_year_data[subject_name][year] = count
                all_years.add(year)

        # 计算每个学科的总发文数并排序
        subject_totals = []
        for subject, yearly_data in subject_year_data.items():
            total = sum(yearly_data.values())
            subject_totals.append((subject, total, yearly_data))

        # 按总发文数从高到低排序
        subject_totals.sort(key=lambda x: x[1], reverse=True)

        # 添加排名
        ranked_data = []
        for rank, (subject, total, yearly_data) in enumerate(subject_totals, 1):
            ranked_data.append(
                {
                    "rank": rank,
                    "subject": subject,
                    "total": total,
                    "yearly_data": yearly_data,
                }
            )

        # 确保年份按顺序排列
        sorted_years = sorted(list(all_years))

        context["ranked_data"] = ranked_data
        context["years"] = sorted_years
        context["title"] = "学科布局排名"

        return context


class QuadrantView(LoginRequiredMixin, TemplateView):
    template_name = "indicators/quadrant.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        """四象限分析页面视图"""
        # 获取年份参数
        year = self.request.GET.get("year")
        if year:
            year = int(year)

        years = sorted(set(SubjectData.objects.values_list("year", flat=True)))

        # 计算四象限数据
        quadrant_data = {"datasets": []}
        data = self.calculate_quadrant_data(year)
        for d in data["data_points"]:
            color = self.get_color_for_subject(d["quadrant"])

            dataset = {
                "label": d["subject"],
                "data": [{"x": d["influence"], "y": d["growth"], "name": d["subject"]}],
                "borderColor": color["border"],  # 需要实现颜色分配
                "backgroundColor": color["bg"],
                "borderWidth": 2,
                "pointRadius": 8,
                "pointHoverRadius": 12,
            }

            quadrant_data["datasets"].append(dataset)

        context["quadrant_data"] = json.dumps(quadrant_data)
        context["years"] = list(years)
        context["title"] = "学科演化分析"

        return context

    def calculate_quadrant_data(self, reference_year=None):
        """计算四象限数据"""
        if not reference_year:
            # 获取最新的年份作为参考年份
            latest_entry = SubjectData.objects.order_by("-year").first()
            reference_year = latest_entry.year if latest_entry else datetime.now().year

        # 获取所有学科
        subjects = PrimarySubject.objects.all()

        # 计算每个学科的影响力和增长率
        subject_metrics = []

        for subject in subjects:
            # 获取最近5年的数据用于计算增长率
            # recent_data = SubjectData.objects.filter(
            #     subject=subject, year__lte=reference_year, year__gte=reference_year - 4
            # ).order_by("year")
            recent_data = (
                SubjectData.objects.values("year")
                .filter(
                    primary_subject_id=subject.code,
                    year__lte=reference_year,
                    year__gte=reference_year - 4,
                )
                .annotate(count=Count("id"))
                .order_by("-year")
            )

            if not recent_data.exists():
                continue

            # 计算影响力（综合指标）
            # latest_data = recent_data.last()
            # influence_score = (
            #     latest_data.paper_count * 0.3
            #     + latest_data.citation_count * 0.5
            #     + latest_data.collaboration_count * 0.1
            #     + latest_data.funding_amount * 0.1
            # )
            influence_score = sum(item["count"] for item in recent_data)

            # 计算增长率（基于最近5年的数据）
            if recent_data.count() >= 2:
                first_year_count = recent_data.first()["count"]
                last_year_count = recent_data.last()["count"]
                if first_year_count > 0:
                    growth_rate = (
                        (last_year_count - first_year_count) / first_year_count
                    ) * 100
                else:
                    growth_rate = 100 if last_year_count > 0 else 0
            else:
                growth_rate = 0

            subject_metrics.append(
                {
                    "subject": subject.name,
                    "influence": round(influence_score, 2),
                    "growth": round(growth_rate, 2),
                    "quadrant": 0,
                    # "papers": latest_data.paper_count,
                    # "citations": latest_data.citation_count,
                }
            )

        # 计算平均值作为象限分割线
        if subject_metrics:
            avg_influence = sum(item["influence"] for item in subject_metrics) / len(
                subject_metrics
            )
            avg_growth = sum(item["growth"] for item in subject_metrics) / len(
                subject_metrics
            )
        else:
            avg_influence = 0
            avg_growth = 0

        # 分类到四个象限
        quadrants = {
            "first": [],  # 高增长-高影响 (明星学科)
            "second": [],  # 低增长-高影响 (成熟学科)
            "third": [],  # 低增长-低影响 (衰退学科)
            "fourth": [],  # 高增长-低影响 (新兴学科)
        }

        for metric in subject_metrics:
            if metric["growth"] >= avg_growth and metric["influence"] >= avg_influence:
                quadrants["first"].append(metric)
                metric["quadrant"] = 1
            elif metric["growth"] < avg_growth and metric["influence"] >= avg_influence:
                quadrants["second"].append(metric)
                metric["quadrant"] = 2
            elif metric["growth"] < avg_growth and metric["influence"] < avg_influence:
                quadrants["third"].append(metric)
                metric["quadrant"] = 3
            else:
                quadrants["fourth"].append(metric)
                metric["quadrant"] = 4

        # 按影响力排序
        for quadrant in quadrants:
            quadrants[quadrant].sort(key=lambda x: x["influence"], reverse=True)

        return {
            "data_points": subject_metrics,
            "averages": {
                "influence": round(avg_influence, 2),
                "growth": round(avg_growth, 2),
            },
            "quadrants": quadrants,
            "year": reference_year,
            "total_subjects": len(subject_metrics),
        }

    def get_color_for_subject(self, quadrant):
        colors = {
            1: {"bg": "rgba(255, 99, 132, 0.6)", "border": "rgba(255, 99, 132, 1)"},
            2: {"bg": "rgba(54, 162, 235, 0.6)", "border": "rgba(54, 162, 235, 1)"},
            3: {"bg": "rgba(255, 206, 86, 0.6)", "border": "rgba(255, 206, 86, 1)"},
            4: {"bg": "rgba(75, 192, 192, 0.6)", "border": "rgba(75, 192, 192, 1)"},
        }

        return colors[quadrant]
