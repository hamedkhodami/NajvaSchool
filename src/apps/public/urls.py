from django.urls import path

from .views import HomeView, NewsDetailView, NewsListView


app_name = "public"

urlpatterns = [
    path("", HomeView.as_view(), name="index"),
    path("news/", NewsListView.as_view(), name="news_list"),
    path("news/<uuid:id>/", NewsDetailView.as_view(), name="news_detail"),
]
