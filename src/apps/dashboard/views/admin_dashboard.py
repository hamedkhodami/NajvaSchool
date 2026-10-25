from django.contrib.auth import get_user_model
from django.shortcuts import render
from django.views import View

from apps.academic.models import AcademicYearModel, ClassroomModel, SubjectModel
from apps.finance.models import SchoolExpenseModel, TuitionModel
from apps.student.models import StudentModel
from apps.teacher.models import TeacherModel


User = get_user_model()


class AdminUserDashboardView(View):
    template_name = "dashboard/admin/user_dashboard.html"

    def get(self, request):
        total_users = User.objects.count()

        context = {
            "total_users": total_users,
            "user_list_url": "account:user_list",
        }

        return render(request, self.template_name, context)


class AdminTeacherDashboardView(View):
    template_name = "dashboard/admin/teacher_dashboard.html"

    def get(self, request):
        total_teachers = TeacherModel.objects.count()

        context = {
            "total_teachers": total_teachers,
        }
        return render(request, self.template_name, context)


class AdminStudentDashboardView(View):
    template_name = "dashboard/admin/student_dashboard.html"

    def get(self, request):
        total_students = StudentModel.objects.count()

        context = {
            "total_students": total_students,
        }
        return render(request, self.template_name, context)


class AdminAcademicDashboardView(View):
    template_name = "dashboard/admin/academic_dashboard.html"

    def get(self, request):
        context = {
            "total_years": AcademicYearModel.objects.count(),
            "total_classrooms": ClassroomModel.objects.count(),
            "total_subjects": SubjectModel.objects.count(),
        }
        return render(request, self.template_name, context)


class AdminFinanceDashboardView(View):
    template_name = "dashboard/admin/finance_dashboard.html"

    def get(self, request):
        has_finance_data = (
            TuitionModel.objects.exists() or SchoolExpenseModel.objects.exists()
        )

        context = {
            "has_finance_data": has_finance_data,
        }
        return render(request, self.template_name, context)
