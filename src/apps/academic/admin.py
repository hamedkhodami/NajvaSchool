from django.contrib import admin

from apps.academic.models import (
    AcademicYearModel,
    ClassroomModel,
    ScheduleSessionModel,
    SubjectModel,
)


@admin.register(AcademicYearModel)
class AcademicYearAdmin(admin.ModelAdmin):
    list_display = (
        "name",
        "start_date",
        "end_date",
        "status",
        "created_at",
    )

    list_display_links = ("name",)

    list_filter = ("status",)

    search_fields = ("name",)

    readonly_fields = (
        "id",
        "created_at",
        "updated_at",
    )

    ordering = ("-start_date",)

    date_hierarchy = "start_date"


@admin.register(ClassroomModel)
class ClassroomAdmin(admin.ModelAdmin):
    list_display = (
        "name",
        "grade",
        "academic_year",
        "capacity",
        "status",
        "created_at",
    )

    list_display_links = ("name",)

    list_filter = (
        "status",
        "academic_year",
        "grade",
    )

    search_fields = (
        "name",
        "grade__name",
        "academic_year__name",
    )

    readonly_fields = (
        "id",
        "created_at",
        "updated_at",
    )

    autocomplete_fields = ("academic_year",)

    ordering = ("-created_at",)


@admin.register(SubjectModel)
class SubjectAdmin(admin.ModelAdmin):
    list_display = (
        "name",
        "code",
        "description",
        "created_at",
    )

    list_display_links = (
        "name",
        "code",
    )

    search_fields = (
        "name",
        "code",
    )

    readonly_fields = (
        "id",
        "created_at",
        "updated_at",
    )

    ordering = ("name",)


@admin.register(ScheduleSessionModel)
class ScheduleSessionAdmin(admin.ModelAdmin):
    list_display = (
        "classroom",
        "subject",
        "teacher",
        "weekday",
        "session_number",
        "created_at",
    )

    list_display_links = (
        "classroom",
        "subject",
    )

    list_filter = (
        "weekday",
        "classroom__academic_year",
        "classroom__grade",
        "subject",
        "teacher",
    )

    search_fields = (
        "classroom__name",
        "classroom__code",
        "subject__name",
        "subject__code",
        "teacher__user__first_name",
        "teacher__user__last_name",
        "teacher__national_id",
    )

    readonly_fields = (
        "id",
        "created_at",
        "updated_at",
    )

    autocomplete_fields = (
        "classroom",
        "subject",
        "teacher",
    )

    ordering = (
        "weekday",
        "session_number",
    )
