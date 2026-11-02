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
    path(
        "teacher/absences/create/",
        admin.AdminTeacherAbsenceCreateView.as_view(),
        name="admin_teacher_absence_create",
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
    path(
        "teacher/attendance/session/<uuid:schedule_id>/lists/",
        teacher.TeacherAttendanceListsView.as_view(),
        name="teacher_attendance_lists",
    ),
    path(
        "teacher/attendance/session/<uuid:schedule_id>/lists/<uuid:attendance_session_id>/",
        teacher.TeacherAttendanceListDetailView.as_view(),
        name="teacher_attendance_list_detail",
    ),
]
