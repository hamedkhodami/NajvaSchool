from django.shortcuts import redirect, render
from django.views import View
from django.views.generic import DetailView, ListView

from apps.academic.models import ScheduleSessionModel
from apps.academic.services.active_year import get_active_year
from apps.account.enums import UserRoleEnum
from apps.account.forms import UserCreationForm
from apps.account.mixins import AdminRequiredMixin
from apps.teacher.forms import TeacherCreationForm
from apps.teacher.models import TeacherModel


class CreateTeacherUserView(AdminRequiredMixin, View):
    template_name = "teacher/admin/create_teacher.html"

    def get(self, request):
        return render(
            request,
            self.template_name,
            {
                "user_form": UserCreationForm(),
                "teacher_form": TeacherCreationForm(),
            },
        )

    def post(self, request):
        user_form = UserCreationForm(request.POST)
        teacher_form = TeacherCreationForm(request.POST)

        if not user_form.is_valid() or not teacher_form.is_valid():
            return render(
                request,
                self.template_name,
                {
                    "user_form": user_form,
                    "teacher_form": teacher_form,
                },
            )

        user = user_form.save(commit=False)
        user.set_password(user_form.cleaned_data["password1"])
        user.is_verified = True
        user.role = UserRoleEnum.TEACHER
        user.save()

        teacher = teacher_form.save(commit=False)
        teacher.user = user
        teacher.save()

        return redirect("dashboard:dashboard")


class TeacherListView(AdminRequiredMixin, ListView):
    model = TeacherModel
    template_name = "teacher/admin/teacher_list.html"
    context_object_name = "teachers"


class TeacherDetailView(AdminRequiredMixin, DetailView):
    model = TeacherModel
    template_name = "teacher/admin/teacher_detail.html"
    context_object_name = "teacher"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        teacher = self.object
        active_year = get_active_year(self.request)

        sessions = ScheduleSessionModel.objects.filter(
            teacher=teacher, classroom__academic_year=active_year
        ).select_related("classroom", "subject")

        classrooms = {s.classroom for s in sessions}

        context["active_year"] = active_year
        context["classrooms"] = classrooms
        context["sessions"] = sessions
        return context
