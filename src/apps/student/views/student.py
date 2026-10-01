from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import get_object_or_404
from django.views.generic import DetailView

from apps.student.models import StudentModel


class StudentProfileView(LoginRequiredMixin, DetailView):
    model = StudentModel
    template_name = "student/profile.html"
    context_object_name = "student"

    def get_object(self):
        user = self.request.user

        return get_object_or_404(StudentModel, user=user)
