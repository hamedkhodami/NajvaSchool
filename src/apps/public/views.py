from django.shortcuts import get_object_or_404, render
from django.views import View

from apps.core.pagination import paginate_queryset
from apps.public.models import AboutUsModel, ContactInfoModel, NewsModel


class HomeView(View):
    def get(self, request):
        about = AboutUsModel.objects.order_by("-updated_at").first()
        contact = ContactInfoModel.objects.order_by("-updated_at").first()
        news = NewsModel.objects.filter(is_published=True).order_by("-published_at")[:3]

        context = {
            "about": about,
            "contact": contact,
            "news": news,
        }

        return render(request, "public/index.html", context)


class NewsListView(View):

    def get(self, request):
        news = NewsModel.objects.filter(
            is_published=True,
        ).order_by("-published_at", "-id")

        pagination = paginate_queryset(
            request=request,
            queryset=news,
            per_page=10,
        )

        return render(
            request,
            "public/news_list.html",
            {
                "news": pagination["object_list"],
                "paginator": pagination["paginator"],
                "page_obj": pagination["page_obj"],
                "is_paginated": pagination["is_paginated"],
            },
        )


class NewsDetailView(View):
    def get(self, request, id):
        item = get_object_or_404(NewsModel, id=id, is_published=True)
        return render(request, "public/news_detail.html", {"item": item})
