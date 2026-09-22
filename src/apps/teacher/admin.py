from django.contrib import admin

from apps.teacher.models import (
    EmploymentRecordModel,
    TeacherModel,
    TeacherNoteModel,
)


@admin.register(TeacherModel)
class TeacherAdmin(admin.ModelAdmin):
    list_display = (
        "id",
        "national_id",
        "get_full_name",
        "status",
        "employment_type",
        "education",
        "specialization",
        "created_at",
    )

    list_display_links = (
        "id",
        "national_id",
        "get_full_name",
    )

    list_filter = (
        "status",
        "employment_type",
        "education",
        "created_at",
    )

    search_fields = (
        "national_id",
        "user__phone_number",
        "user__first_name",
        "user__last_name",
        "education",
        "specialization",
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
            "اطلاعات شغلی",
            {
                "fields": (
                    "national_id",
                    "status",
                    "employment_type",
                    "education",
                    "specialization",
                )
            },
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


@admin.register(TeacherNoteModel)
class TeacherNoteAdmin(admin.ModelAdmin):
    list_display = (
        "id",
        "teacher",
        "attendance_session",
        "title",
        "created_at",
        "updated_at",
    )

    list_display_links = (
        "id",
        "title",
    )

    search_fields = (
        "title",
        "content",
        "teacher__national_id",
        "teacher__user__first_name",
        "teacher__user__last_name",
    )

    list_filter = (
        "created_at",
        "updated_at",
    )

    readonly_fields = (
        "created_at",
        "updated_at",
        "deleted_at",
    )

    autocomplete_fields = ("teacher",)

    fieldsets = (
        (
            "اطلاعات یادداشت",
            {
                "fields": (
                    "teacher",
                    "attendance_session",
                    "title",
                    "content",
                )
            },
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

    ordering = ("-created_at",)

    date_hierarchy = "created_at"


@admin.register(EmploymentRecordModel)
class EmploymentRecordAdmin(admin.ModelAdmin):
    list_display = (
        "id",
        "teacher",
        "employment_type",
        "start_date",
        "end_date",
        "created_at",
    )

    list_display_links = (
        "id",
        "teacher",
    )

    list_filter = (
        "employment_type",
        "start_date",
        "end_date",
    )

    search_fields = (
        "teacher__national_id",
        "teacher__user__first_name",
        "teacher__user__last_name",
        "description",
    )

    readonly_fields = (
        "created_at",
        "updated_at",
        "deleted_at",
    )

    autocomplete_fields = ("teacher",)

    fieldsets = (
        (
            "اطلاعات همکاری",
            {
                "fields": (
                    "teacher",
                    "employment_type",
                    "start_date",
                    "end_date",
                    "description",
                )
            },
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

    ordering = ("-start_date",)

    date_hierarchy = "start_date"
