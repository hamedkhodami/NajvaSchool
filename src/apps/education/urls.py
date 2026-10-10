from django.urls import path

from apps.education.views import exam, exam_result


app_name = "education"

urlpatterns = [
    # Exam
    path("exams/create/", exam.TeacherExamCreateView.as_view(), name="exam_create"),
    path("exams/", exam.TeacherExamListView.as_view(), name="exam_list"),
    path(
        "exams/<uuid:exam_id>/",
        exam.TeacherExamDetailView.as_view(),
        name="exam_detail",
    ),
    path(
        "exams/<uuid:exam_id>/edit/",
        exam.TeacherExamUpdateView.as_view(),
        name="exam_edit",
    ),
    path("question-bank/", exam.QuestionBankListView.as_view(), name="question_bank"),
    # Exam Result
    path(
        "exams/<uuid:exam_id>/results/",
        exam_result.TeacherExamResultView.as_view(),
        name="exam_results",
    ),
]
