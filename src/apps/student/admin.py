from django.contrib import admin

from apps.student.models import StudentModel


@admin.register(StudentModel)
class StudentAdmin(admin.ModelAdmin):
    list_display = (
        "id",
        "national_id",
        "get_full_name",
        "father_name",
        "parent_phone_number",
        "status",
        "created_at",
    )

    list_display_links = (
        "id",
        "national_id",
        "get_full_name",
    )

    list_filter = (
        "status",
        "created_at",
    )

    search_fields = (
        "national_id",
        "user__phone_number",
        "user__first_name",
        "user__last_name",
        "father_name",
        "parent_phone_number",
    )

    readonly_fields = (
        "created_at",
        "updated_at",
        "deleted_at",
    )

    autocomplete_fields = ("user",)

    fieldsets = (
        (
            "اطلاعات حساب کاربری",
            {"fields": ("user",)},
        ),
        (
            "اطلاعات دانش‌آموز",
            {
                "fields": (
                    "national_id",
                    "father_name",
                    "parent_phone_number",
                    "birth_date",
                    "address",
                )
            },
        ),
        (
            "وضعیت تحصیلی",
            {"fields": ("status",)},
        ),
        (
            "اطلاعات سیستمی",
            {
                "fields": (
                    "created_at",
                    "updated_at",
                    "deleted_at",
                    "is_deleted",
                )
            },
        ),
    )

    ordering = (
        "user__first_name",
        "user__last_name",
    )

    date_hierarchy = "created_at"

    def get_full_name(self, obj):
        return obj.user.full_name

    get_full_name.short_description = "نام و نام خانوادگی"
