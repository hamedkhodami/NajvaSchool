from django.contrib import admin

from apps.public.models import AboutUsModel, ContactInfoModel, NewsModel


@admin.register(AboutUsModel)
class AboutUsAdmin(admin.ModelAdmin):
    list_display = (
        "id",
        "created_at",
        "updated_at",
    )

    readonly_fields = (
        "created_at",
        "updated_at",
    )


@admin.register(ContactInfoModel)
class ContactInfoAdmin(admin.ModelAdmin):
    list_display = (
        "id",
        "phone_number",
        "mobile_number",
        "school_number",
        "created_at",
        "updated_at",
    )

    readonly_fields = (
        "created_at",
        "updated_at",
    )


@admin.register(NewsModel)
class NewsAdmin(admin.ModelAdmin):
    list_display = (
        "title",
        "is_published",
        "published_at",
        "created_at",
    )

    list_filter = (
        "is_published",
        "published_at",
    )

    search_fields = (
        "title",
        "content",
    )

    readonly_fields = (
        "created_at",
        "updated_at",
    )

    ordering = (
        "-published_at",
        "-created_at",
    )
