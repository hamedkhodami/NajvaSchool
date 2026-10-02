from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import TemplateView

from apps.academic.models import ScheduleSessionModel
from apps.academic.services.active_year import get_active_year
from apps.account.enums import UserRoleEnum


class DashboardView(LoginRequiredMixin, TemplateView):
    template_name = "dashboard/dashboard.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        user = self.request.user

        # نقش کاربر
        if user.is_superuser:
            role = UserRoleEnum.ADMIN
        elif hasattr(user, "role"):
            role = user.role
        else:
            role = "unknown"

        context["role"] = role

        # داده‌های اختصاصی هر نقش
        if role == UserRoleEnum.TEACHER:
            teacher = getattr(user, "teacher", None)
            active_year = get_active_year(self.request)
            if teacher and active_year:
                sessions = ScheduleSessionModel.objects.filter(
                    teacher=teacher, classroom__academic_year=active_year
                ).select_related("classroom", "subject")
                context["teacher"] = teacher
                context["active_year"] = active_year
                context["sessions"] = sessions

        elif role == UserRoleEnum.STUDENT:
            student = getattr(user, "student", None)
            active_year = get_active_year(self.request)
            if student and active_year:
                classrooms = student.classrooms.filter(academic_year=active_year)
                sessions = ScheduleSessionModel.objects.filter(
                    classroom__in=classrooms
                ).select_related("subject", "teacher")
                context["student"] = student
                context["active_year"] = active_year
                context["classrooms"] = classrooms
                context["sessions"] = sessions

        return context
