from django.urls import path

from apps.education.views import daily_grade, exam, exam_result


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
    path(
        "teacher/classes/",
        exam_result.TeacherClassListView.as_view(),
        name="teacher_class_list",
    ),
    path(
        "teacher/classes/<uuid:classroom_id>/exams/",
        exam_result.TeacherClassExamResultView.as_view(),
        name="teacher_class_exam_results",
    ),
    path(
        "student/exams/",
        exam_result.StudentExamResultListView.as_view(),
        name="student_exam_results",
    ),
    # daily grade
    path(
        "teacher/daily-grade/classes/",
        daily_grade.TeacherDailyGradeClassListView.as_view(),
        name="teacher_daily_grade_class_list",
    ),
    path(
        "teacher/daily-grade/create/<uuid:classroom_id>/",
        daily_grade.TeacherDailyGradeCreateView.as_view(),
        name="teacher_daily_grade_create",
    ),
    path(
        "teacher/daily-grade/list/<uuid:classroom_id>/",
        daily_grade.TeacherDailyGradeListView.as_view(),
        name="teacher_daily_grade_list",
    ),
    path(
        "student/daily-grades/",
        daily_grade.StudentDailyGradeListView.as_view(),
        name="student_daily_grade_list",
    ),
]
