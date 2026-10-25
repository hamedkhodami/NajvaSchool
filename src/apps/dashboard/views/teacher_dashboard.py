from django.views.generic import TemplateView

from apps.academic.models import ClassroomModel
from apps.academic.services.active_year import get_active_year
from apps.teacher.mixins import TeacherRequiredMixin


class TeacherClassesDashboardView(TeacherRequiredMixin, TemplateView):
    template_name = "dashboard/teacher/classes_dashboard.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        teacher = self.request.user.teacher
        active_year = get_active_year(self.request)

        # کلاس‌هایی که این معلم در سال فعال دارد
        classes = ClassroomModel.objects.filter(
            schedule_sessions__teacher=teacher, academic_year=active_year
        ).distinct()

        context["teacher"] = teacher
        context["active_year"] = active_year
        context["classes"] = classes

        return context
