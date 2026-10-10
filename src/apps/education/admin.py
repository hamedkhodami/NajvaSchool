from django.contrib import admin

from apps.education.models import (
    DailyGradeModel,
    EducationalActivityModel,
    ExamModel,
    ExamResultModel,
)


@admin.register(ExamModel)
class ExamAdmin(admin.ModelAdmin):
    list_display = (
        "id",
        "classroom",
        "subject",
        "teacher",
        "max_score",
        "is_published",
    )

    list_display_links = ("id",)

    list_filter = (
        "is_published",
        "subject",
        "classroom",
        "teacher",
    )

    search_fields = (
        "title",
        "subject__name",
        "teacher__user__first_name",
        "teacher__user__last_name",
        "teacher__national_id",
    )

    autocomplete_fields = (
        "classroom",
        "subject",
        "teacher",
    )

    ordering = ("-created_at",)


@admin.register(ExamResultModel)
class ExamResultAdmin(admin.ModelAdmin):
    list_display = (
        "id",
        "exam",
        "student",
        "score",
        "created_at",
    )

    list_display_links = (
        "id",
        "student",
    )

    list_filter = (
        "exam",
        "exam__subject",
        "exam__classroom",
    )

    search_fields = (
        "student__national_id",
        "student__user__first_name",
        "student__user__last_name",
    )

    autocomplete_fields = (
        "exam",
        "student",
    )

    ordering = ("-created_at",)


@admin.register(DailyGradeModel)
class DailyGradeAdmin(admin.ModelAdmin):
    list_display = (
        "id",
        "student",
        "subject",
        "teacher",
        "classroom",
        "attendance_session",
        "title",
        "score",
        "created_at",
    )

    list_display_links = (
        "id",
        "student",
    )

    list_filter = (
        "subject",
        "teacher",
        "classroom",
        "attendance_session",
    )

    search_fields = (
        "title",
        "student__national_id",
        "student__user__first_name",
        "student__user__last_name",
        "teacher__user__first_name",
        "teacher__user__last_name",
        "subject__name",
    )

    autocomplete_fields = (
        "student",
        "teacher",
        "classroom",
        "subject",
    )

    ordering = ("-created_at",)


@admin.register(EducationalActivityModel)
class EducationalActivityAdmin(admin.ModelAdmin):
    list_display = (
        "id",
        "title",
        "activity_type",
        "classroom",
        "subject",
        "teacher",
        "attendance_session",
        "created_at",
    )

    list_display_links = (
        "id",
        "title",
    )

    list_filter = (
        "activity_type",
        "subject",
        "teacher",
        "classroom",
        "attendance_session",
    )

    search_fields = (
        "title",
        "description",
        "classroom__name",
        "subject__name",
        "teacher__user__first_name",
        "teacher__user__last_name",
        "teacher__national_id",
    )

    autocomplete_fields = (
        "classroom",
        "subject",
        "teacher",
    )

    ordering = ("-created_at",)
