from django.urls import path

from apps.finance.views import expense, payment, salary, tuition


app_name = "finance"

urlpatterns = [
    # Tuition
    path("tuition/create/", tuition.TuitionCreateView.as_view(), name="tuition_create"),
    path("tuition/list/", tuition.TuitionListView.as_view(), name="tuition_list"),
    path(
        "tuition/<uuid:tuition_id>/detail/",
        tuition.TuitionDetailView.as_view(),
        name="tuition_detail",
    ),
    path(
        "student/tuition/status/",
        tuition.StudentTuitionStatusView.as_view(),
        name="student_tuition_status",
    ),
    # payment
    path(
        "tuition/<uuid:tuition_id>/payment/create/",
        payment.TuitionPaymentCreateView.as_view(),
        name="tuition_payment_create",
    ),
    # salary
    # apps/finance/urls.py
    path(
        "salary/create/",
        salary.StaffSalaryCreateView.as_view(),
        name="salary_create",
    ),
    path("salary/list/", salary.StaffSalaryListView.as_view(), name="salary_list"),
    path(
        "salary/<uuid:salary_id>/update/",
        salary.StaffSalaryUpdateView.as_view(),
        name="salary_update",
    ),
    path(
        "salary/monthly/prepare/",
        salary.MonthlySalaryPrepareView.as_view(),
        name="salary_monthly_prepare",
    ),
    path(
        "salary/monthly/export/",
        salary.MonthlySalaryExportView.as_view(),
        name="salary_monthly_export",
    ),
    path(
        "salary/<uuid:salary_id>/payment/create/",
        salary.SalaryPaymentCreateView.as_view(),
        name="salary_payment_create",
    ),
    path(
        "salary/<uuid:salary_id>/detail/",
        salary.StaffSalaryDetailView.as_view(),
        name="salary_detail",
    ),
    path(
        "salary/dashboard/",
        salary.TeacherSalaryDashboardView.as_view(),
        name="teacher_salary_dashboard",
    ),
    # Expose
    path("expense/list/", expense.ExpenseListView.as_view(), name="expense_list"),
    path("expense/create/", expense.ExpenseCreateView.as_view(), name="expense_create"),
    path(
        "expense/<uuid:expense_id>/update/",
        expense.ExpenseUpdateView.as_view(),
        name="expense_update",
    ),
    path(
        "expense/<uuid:expense_id>/delete/",
        expense.ExpenseDeleteView.as_view(),
        name="expense_delete",
    ),
]
