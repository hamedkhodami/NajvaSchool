from django.contrib import messages
from django.shortcuts import get_object_or_404, redirect, render
from django.views import View

from apps.academic.models import ClassroomModel
from apps.academic.services.active_year import get_active_year
from apps.account.mixins import AdminRequiredMixin
from apps.discipline.models import StudentDevelopmentRecordModel
from apps.student.models import StudentModel


class AdminRewardCreateView(AdminRequiredMixin, View):
    template_name = "discipline/admin_reward_create.html"

    def get(self, request, classroom_id):
        classroom = get_object_or_404(ClassroomModel, id=classroom_id)
        students = classroom.students.all()

        return render(
            request,
            self.template_name,
            {
                "classroom": classroom,
                "students": students,
            },
        )

    def post(self, request, classroom_id):
        classroom = get_object_or_404(ClassroomModel, id=classroom_id)
        students = classroom.students.all()

        title = request.POST.get("title")
        description = request.POST.get("description")
        date = request.POST.get("date")

        selected_ids = request.POST.getlist("students")

        if not selected_ids:
            messages.error(request, "هیچ دانش‌آموزی انتخاب نشده است.")
            return redirect("discipline:admin_reward_create", classroom_id=classroom.id)

        for sid in selected_ids:
            student = get_object_or_404(StudentModel, id=sid)

            StudentDevelopmentRecordModel.objects.create(
                student=student,
                recorder=request.user,
                classroom=classroom,
                category="discipline",
                effect="positive",
                title=title,
                description=description,
                date=date,
            )

        messages.success(request, "تشویقی‌ها با موفقیت ثبت شدند.")
        return redirect("discipline:admin_reward_list")


class AdminRewardListView(AdminRequiredMixin, View):
    template_name = "discipline/admin_reward_list.html"

    def get(self, request):
        active_year = get_active_year(request)

        records = StudentDevelopmentRecordModel.objects.filter(
            effect="positive", classroom__academic_year=active_year
        ).select_related("student", "classroom", "recorder")

        return render(
            request,
            self.template_name,
            {
                "records": records,
                "active_year": active_year,
            },
        )


class AdminRewardDetailView(AdminRequiredMixin, View):
    template_name = "discipline/admin_reward_detail.html"

    def get(self, request, record_id):
        record = get_object_or_404(StudentDevelopmentRecordModel, id=record_id)
        return render(request, self.template_name, {"record": record})

    def post(self, request, record_id):
        record = get_object_or_404(StudentDevelopmentRecordModel, id=record_id)

        record.title = request.POST.get("title")
        record.description = request.POST.get("description")
        record.date = request.POST.get("date")
        record.save()

        messages.success(request, "تشویقی با موفقیت بروزرسانی شد.")
        return redirect("discipline:admin_reward_detail", record_id=record.id)


class AdminRewardDeleteView(AdminRequiredMixin, View):
    def post(self, request, record_id):
        record = get_object_or_404(StudentDevelopmentRecordModel, id=record_id)
        record.delete()
        messages.success(request, "تشویقی حذف شد.")
        return redirect("discipline:admin_reward_list")
