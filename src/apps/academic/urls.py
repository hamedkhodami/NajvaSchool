from django.urls import path

from apps.academic.views import academic


app_name = "academic"

urlpatterns = [
    path(
        "academic-years/",
        academic.AcademicYearListCreateView.as_view(),
        name="academic_year_list",
    ),
]
