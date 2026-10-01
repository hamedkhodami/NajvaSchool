from django.urls import path

from apps.academic.views import academic, grade


app_name = "academic"

urlpatterns = [
    path(
        "academic-years/",
        academic.AcademicYearListView.as_view(),
        name="academic_year_list",
    ),
    path(
        "academic-years/create/",
        academic.AcademicYearCreateView.as_view(),
        name="academic_year_create",
    ),
    path(
        "academic-years/<uuid:year_id>/update-status/",
        academic.AcademicYearUpdateStatusView.as_view(),
        name="academic_year_update_status",
    ),
    path(
        "academic-years/<uuid:year_id>/activate/",
        academic.AcademicYearActivateView.as_view(),
        name="academic_year_activate",
    ),
    # grade
    path("classrooms/", grade.ClassroomListView.as_view(), name="classroom_list"),
    path(
        "classrooms/create/",
        grade.ClassroomCreateView.as_view(),
        name="classroom_create",
    ),
    path(
        "classrooms/<uuid:class_id>/update/",
        grade.ClassroomUpdateView.as_view(),
        name="classroom_update",
    ),
    path(
        "classrooms/<uuid:class_id>/delete/",
        grade.ClassroomDeleteView.as_view(),
        name="classroom_delete",
    ),
]
