from django.contrib import admin

from apps.discipline.models import StudentDevelopmentRecordModel


@admin.register(StudentDevelopmentRecordModel)
class StudentDevelopmentRecordAdmin(admin.ModelAdmin):
    list_display = (
        "id",
        "student",
        "category",
        "effect",
        "level",
        "educational_type",
        "title",
        "recorder",
        "classroom",
        "date",
        "created_at",
    )

    list_display_links = (
        "id",
        "student",
        "title",
    )

    list_filter = (
        "category",
        "effect",
        "level",
        "educational_type",
        "date",
        "classroom",
    )

    search_fields = (
        "student__user__first_name",
        "student__user__last_name",
        "student__national_id",
        "title",
        "description",
    )

    autocomplete_fields = (
        "student",
        "recorder",
        "classroom",
    )

    date_hierarchy = "date"

    ordering = (
        "-date",
        "-created_at",
    )

    readonly_fields = (
        "created_at",
        "updated_at",
    )
