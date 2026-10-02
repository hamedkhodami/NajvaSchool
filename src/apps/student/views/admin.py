from django.db.models import Q
from django.shortcuts import redirect, render
from django.views import View
from django.views.generic import DetailView, ListView

from apps.academic.models import ScheduleSessionModel
from apps.academic.services.active_year import get_active_year
from apps.account.enums import UserRoleEnum
from apps.account.forms import UserCreationForm
from apps.account.mixins import AdminRequiredMixin
from apps.student.forms import StudentCreationForm
from apps.student.models import StudentModel


class StudentListView(AdminRequiredMixin, ListView):
    model = StudentModel
    template_name = "student/admin/student_list.html"
    context_object_name = "students"

    def get_queryset(self):
        qs = super().get_queryset()

        search = self.request.GET.get("search")

        if search:
            qs = qs.filter(
                Q(user__first_name__icontains=search)
                | Q(user__last_name__icontains=search)
                | Q(user__phone_number__icontains=search)
            )

        return qs


class StudentDetailView(AdminRequiredMixin, DetailView):
    model = StudentModel
    template_name = "student/admin/student_detail.html"
    context_object_name = "student"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        student = self.object
        active_year = get_active_year(self.request)

        classrooms = student.classrooms.filter(academic_year=active_year)

        sessions = ScheduleSessionModel.objects.filter(
            classroom__in=classrooms
        ).select_related("subject", "teacher")

        context["active_year"] = active_year
        context["classrooms"] = classrooms
        context["sessions"] = sessions
        return context


class CreateStudentUserView(AdminRequiredMixin, View):
    template_name = "student/admin/create_student.html"

    def get(self, request):
        return render(
            request,
            self.template_name,
            {
                "user_form": UserCreationForm(),
                "student_form": StudentCreationForm(),
            },
        )

    def post(self, request):
        request.POST._mutable = True
        request.POST["role"] = UserRoleEnum.STUDENT

        user_form = UserCreationForm(request.POST)
        student_form = StudentCreationForm(request.POST)

        if not user_form.is_valid() or not student_form.is_valid():
            return render(
                request,
                self.template_name,
                {
                    "user_form": user_form,
                    "student_form": student_form,
                },
            )

        user = user_form.save(commit=False)
        user.set_password(user_form.cleaned_data["password1"])
        user.is_verified = True
        user.role = UserRoleEnum.STUDENT
        user.save()

        student = student_form.save(commit=False)
        student.user = user
        print(user_form.errors)
        print(student_form.errors)
        student.save()

        return redirect("dashboard:dashboard")
