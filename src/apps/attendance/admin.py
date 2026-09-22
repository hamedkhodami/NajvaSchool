from django.contrib import admin

from apps.attendance.models import (
    AttendanceSessionModel,
    StaffAttendanceModel,
    StudentAttendanceModel,
)


@admin.register(AttendanceSessionModel)
class AttendanceSessionAdmin(admin.ModelAdmin):
    list_display = (
        "id",
        "classroom",
        "schedule_session",
        "date",
        "session_number",
        "created_at",
    )

    list_display_links = (
        "id",
        "classroom",
    )

    list_filter = (
        "date",
        "classroom",
    )

    search_fields = (
        "classroom__name",
        "classroom__code",
    )

    readonly_fields = (
        "created_at",
        "updated_at",
    )

    ordering = (
        "-date",
        "session_number",
    )

    date_hierarchy = "date"


@admin.register(StudentAttendanceModel)
class StudentAttendanceAdmin(admin.ModelAdmin):
    list_display = (
        "id",
        "student",
        "session",
        "status",
        "arrival_time",
        "created_at",
    )

    list_display_links = (
        "id",
        "student",
    )

    list_filter = (
        "status",
        "session__date",
        "session__classroom",
    )

    search_fields = (
        "student__user__first_name",
        "student__user__last_name",
        "student__national_id",
    )

    readonly_fields = (
        "created_at",
        "updated_at",
    )

    ordering = (
        "-session__date",
        "student",
    )


@admin.register(StaffAttendanceModel)
class StaffAttendanceAdmin(admin.ModelAdmin):
    list_display = (
        "id",
        "teacher",
        "date",
        "status",
        "arrival_time",
        "departure_time",
        "created_at",
    )

    list_display_links = (
        "id",
        "teacher",
    )

    list_filter = (
        "status",
        "date",
    )

    search_fields = (
        "teacher__user__first_name",
        "teacher__user__last_name",
        "teacher__national_id",
    )

    readonly_fields = (
        "created_at",
        "updated_at",
    )

    ordering = (
        "-date",
        "teacher",
    )

    date_hierarchy = "date"
