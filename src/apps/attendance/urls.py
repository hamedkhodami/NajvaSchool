from django.urls import path

from apps.attendance.views import admin, teacher


app_name = "attendance"

urlpatterns = [
    # Admin
    path(
        "attendance/absences/",
        admin.AdminAbsenceListView.as_view(),
        name="admin_absence_list",
    ),
    path(
        "attendance/teacher-absences/",
        admin.AdminTeacherAbsenceListView.as_view(),
        name="admin_teacher_absence_list",
    ),
    # Teacher
    path(
        "teacher/attendance/",
        teacher.TeacherAttendanceOverviewView.as_view(),
        name="teacher_attendance_overview",
    ),
    path(
        "teacher/attendance/session/<uuid:schedule_id>/",
        teacher.TeacherAttendanceSessionView.as_view(),
        name="teacher_session",
    ),
    path(
        "teacher/attendance/toggle/",
        teacher.TeacherToggleAttendanceView.as_view(),
        name="teacher_toggle_attendance",
    ),
]
