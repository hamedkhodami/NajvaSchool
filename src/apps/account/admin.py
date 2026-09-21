from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin

from apps.account.forms import UserCreationForm
from apps.account.models import User


@admin.register(User)
class UserAdmin(BaseUserAdmin):
    add_form = UserCreationForm

    list_display = (
        "id",
        "__str__",
        "first_name",
        "last_name",
        "role",
        "is_active",
        "is_verified",
    )

    list_display_links = (
        "id",
        "__str__",
    )

    readonly_fields = (
        "created_at",
        "last_login",
    )

    list_filter = (
        "role",
        "is_active",
        "is_admin",
        "is_verified",
    )

    fieldsets = (
        (
            None,
            {
                "fields": (
                    "phone_number",
                    "password",
                )
            },
        ),
        (
            "اطلاعات شخصی",
            {
                "fields": (
                    "first_name",
                    "last_name",
                    "role",
                )
            },
        ),
        (
            "وضعیت حساب",
            {
                "fields": (
                    "is_active",
                    "is_verified",
                    "is_admin",
                    "is_superuser",
                )
            },
        ),
        (
            "تاریخ‌ها",
            {
                "fields": (
                    "last_login",
                    "created_at",
                )
            },
        ),
    )

    add_fieldsets = (
        (
            None,
            {
                "classes": ("wide",),
                "fields": (
                    "phone_number",
                    "first_name",
                    "last_name",
                    "role",
                    "password1",
                    "password2",
                ),
            },
        ),
    )

    search_fields = (
        "phone_number",
        "first_name",
        "last_name",
    )

    ordering = ("phone_number",)

    date_hierarchy = "created_at"
