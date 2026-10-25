from django.urls import path

from apps.dashboard.views import admin_dashboard, dashboard, teacher_dashboard


app_name = "dashboard"

urlpatterns = [
    path("", dashboard.DashboardView.as_view(), name="dashboard"),
    # Admin
    path(
        "users/",
        admin_dashboard.AdminUserDashboardView.as_view(),
        name="dashboard_users",
    ),
    path(
        "teachers/",
        admin_dashboard.AdminTeacherDashboardView.as_view(),
        name="admin_teacher_dashboard",
    ),
    path(
        "students/",
        admin_dashboard.AdminStudentDashboardView.as_view(),
        name="admin_student_dashboard",
    ),
    path(
        "academic/",
        admin_dashboard.AdminAcademicDashboardView.as_view(),
        name="admin_academic_dashboard",
    ),
    path(
        "finance/",
        admin_dashboard.AdminFinanceDashboardView.as_view(),
        name="admin_finance_dashboard",
    ),
    # Teacher
    path(
        "teacher/classes/",
        teacher_dashboard.TeacherClassesDashboardView.as_view(),
        name="teacher_classes_dashboard",
    ),
]
