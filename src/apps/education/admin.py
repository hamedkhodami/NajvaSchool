from django.contrib import admin

from apps.education.models import (
    AssignmentModel,
    DailyGradeModel,
    EducationalActivityModel,
    ExamModel,
    ExamResultModel,
)


@admin.register(ExamModel)
class ExamAdmin(admin.ModelAdmin):
    list_display = (
        "id",
        "title",
        "classroom",
        "subject",
        "teacher",
        "exam_date",
        "max_score",
        "is_published",
    )

    list_display_links = (
        "id",
        "title",
    )

    list_filter = (
        "is_published",
        "exam_date",
        "subject",
        "classroom",
        "teacher",
    )

    search_fields = (
        "title",
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

    ordering = (
        "-exam_date",
        "-created_at",
    )


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
        "exam__title",
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
        "classroom__name",
    )

    autocomplete_fields = (
        "student",
        "teacher",
        "classroom",
        "subject",
        "attendance_session",
    )

    ordering = ("-created_at",)


@admin.register(AssignmentModel)
class AssignmentAdmin(admin.ModelAdmin):
    list_display = (
        "id",
        "title",
        "classroom",
        "subject",
        "teacher",
        "attendance_session",
        "assigned_at",
        "due_date",
        "status",
    )

    list_display_links = (
        "id",
        "title",
    )

    list_filter = (
        "status",
        "subject",
        "teacher",
        "classroom",
        "assigned_at",
        "due_date",
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
        "attendance_session",
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
        "attendance_session",
    )

    ordering = ("-created_at",)
