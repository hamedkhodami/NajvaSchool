from django.shortcuts import get_object_or_404, render
from django.views import View

from apps.public.models import AboutUsModel, ContactInfoModel, NewsModel


class HomeView(View):
    def get(self, request):
        about = AboutUsModel.objects.order_by("-updated_at").first()
        contact = ContactInfoModel.objects.order_by("-updated_at").first()
        news = NewsModel.objects.filter(is_published=True).order_by("-published_at")[:2]

        context = {
            "about": about,
            "contact": contact,
            "news": news,
        }

        return render(request, "public/index.html", context)


class NewsListView(View):
    def get(self, request):
        news = NewsModel.objects.filter(is_published=True).order_by("-published_at")

        return render(request, "public/news_list.html", {"news": news})


class NewsDetailView(View):
    def get(self, request, id):
        item = get_object_or_404(NewsModel, id=id, is_published=True)
        return render(request, "public/news_detail.html", {"item": item})
