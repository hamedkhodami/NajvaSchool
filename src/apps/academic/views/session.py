from django.shortcuts import get_object_or_404, redirect, render
from django.views import View

from apps.academic.forms import ScheduleSessionForm
from apps.academic.models import ClassroomModel, ScheduleSessionModel
from apps.account.mixins import AdminRequiredMixin


class ScheduleSessionListView(AdminRequiredMixin, View):
    template_name = "academic/session/schedule_session_list.html"

    def get(self, request, class_id):
        classroom = get_object_or_404(ClassroomModel, id=class_id)
        sessions = classroom.schedule_sessions.all()
        return render(
            request, self.template_name, {"classroom": classroom, "sessions": sessions}
        )


class ScheduleSessionCreateView(AdminRequiredMixin, View):
    template_name = "academic/session/schedule_session_create.html"

    def get(self, request, class_id):
        classroom = get_object_or_404(ClassroomModel, id=class_id)
        form = ScheduleSessionForm(classroom=classroom)
        return render(
            request, self.template_name, {"form": form, "classroom": classroom}
        )

    def post(self, request, class_id):
        classroom = get_object_or_404(ClassroomModel, id=class_id)
        form = ScheduleSessionForm(classroom, request.POST)
        if form.is_valid():
            obj = form.save(commit=False)
            obj.classroom = classroom
            obj.save()
            return redirect("academic:schedule_session_list", class_id=classroom.id)
        return render(
            request, self.template_name, {"form": form, "classroom": classroom}
        )


class ScheduleSessionUpdateView(AdminRequiredMixin, View):
    template_name = "academic/session/schedule_session_update.html"

    def get(self, request, session_id):
        session = get_object_or_404(ScheduleSessionModel, id=session_id)
        form = ScheduleSessionForm(session.classroom, instance=session)
        return render(request, self.template_name, {"form": form, "session": session})

    def post(self, request, session_id):
        session = get_object_or_404(ScheduleSessionModel, id=session_id)
        form = ScheduleSessionForm(session.classroom, request.POST, instance=session)
        if form.is_valid():
            form.save()
            return redirect(
                "academic:schedule_session_list", class_id=session.classroom.id
            )
        return render(request, self.template_name, {"form": form, "session": session})


class ScheduleSessionDeleteView(AdminRequiredMixin, View):
    template_name = "academic/session/schedule_session_delete.html"

    def get(self, request, session_id):
        session = get_object_or_404(ScheduleSessionModel, id=session_id)
        return render(request, self.template_name, {"session": session})

    def post(self, request, session_id):
        session = get_object_or_404(ScheduleSessionModel, id=session_id)
        class_id = session.classroom.id
        session.delete()
        return redirect("academic:schedule_session_list", class_id=class_id)
