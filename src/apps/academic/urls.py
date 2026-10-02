from django.urls import path

from apps.academic.views import academic, grade, session, subject


app_name = "academic"

urlpatterns = [
    # academic
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
        "classrooms/<uuid:class_id>/manage-students/",
        grade.ClassroomManageStudentsView.as_view(),
        name="classroom_manage_students",
    ),
    path(
        "classrooms/<uuid:class_id>/remove-student/<uuid:student_id>/",
        grade.ClassroomRemoveStudentView.as_view(),
        name="classroom_remove_student",
    ),
    path(
        "classrooms/<uuid:class_id>/",
        grade.ClassroomDetailView.as_view(),
        name="classroom_detail",
    ),
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
    # subject
    path("subjects/", subject.SubjectListView.as_view(), name="subject_list"),
    path(
        "subjects/create/", subject.SubjectCreateView.as_view(), name="subject_create"
    ),
    path(
        "subjects/<uuid:subject_id>/update/",
        subject.SubjectUpdateView.as_view(),
        name="subject_update",
    ),
    path(
        "subjects/<uuid:subject_id>/delete/",
        subject.SubjectDeleteView.as_view(),
        name="subject_delete",
    ),
    # session
    path(
        "classrooms/<uuid:class_id>/sessions/",
        session.ScheduleSessionListView.as_view(),
        name="schedule_session_list",
    ),
    path(
        "classrooms/<uuid:class_id>/sessions/create/",
        session.ScheduleSessionCreateView.as_view(),
        name="schedule_session_create",
    ),
    path(
        "sessions/<uuid:session_id>/update/",
        session.ScheduleSessionUpdateView.as_view(),
        name="schedule_session_update",
    ),
    path(
        "sessions/<uuid:session_id>/delete/",
        session.ScheduleSessionDeleteView.as_view(),
        name="schedule_session_delete",
    ),
]
