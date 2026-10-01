from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import get_object_or_404
from django.views.generic import DetailView

from apps.teacher.models import TeacherModel


class TeacherProfileView(LoginRequiredMixin, DetailView):
    template_name = "teacher/profile.html"
    context_object_name = "teacher"

    def get_object(self):
        user = self.request.user
        return get_object_or_404(TeacherModel, user=user)
