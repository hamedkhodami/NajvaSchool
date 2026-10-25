from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import get_object_or_404, redirect, render
from django.views import View

from apps.academic.models import ClassroomModel
from apps.academic.services.active_year import get_active_year
from apps.account.mixins import AdminRequiredMixin
from apps.discipline.enums import (
    BehavioralEvaluationLevelEnum,
    DisciplineEffectEnum,
    EducationalRecordTypeEnum,
    StudentRecordCategoryEnum,
)
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
                "record_categories": StudentRecordCategoryEnum.choices,
                "discipline_effects": DisciplineEffectEnum.choices,
                "behavioral_levels": BehavioralEvaluationLevelEnum.choices,
                "educational_types": EducationalRecordTypeEnum.choices,
            },
        )

    def post(self, request, classroom_id):
        classroom = get_object_or_404(ClassroomModel, id=classroom_id)
        students = classroom.students.all()

        title = request.POST.get("title")
        description = request.POST.get("description")

        category = request.POST.get("category")
        effect = request.POST.get("effect")
        level = request.POST.get("level")
        educational_type = request.POST.get("educational_type")

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
                category=category,
                effect=effect,
                level=level,
                educational_type=educational_type,
                title=title,
                description=description,
            )

        messages.success(request, "تشویقی‌ها با موفقیت ثبت شدند.")
        return redirect("discipline:admin_reward_list")


class AdminRewardListView(AdminRequiredMixin, View):
    template_name = "discipline/admin_reward_list.html"

    def get(self, request):
        active_year = get_active_year(request)

        records = StudentDevelopmentRecordModel.objects.filter(
            effect="positive",
            classroom__academic_year=active_year,
            is_deleted=False,  # اگر فیلد حذف نرم داری
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

        return render(
            request,
            self.template_name,
            {
                "record": record,
                "record_categories": StudentRecordCategoryEnum.choices,
                "discipline_effects": DisciplineEffectEnum.choices,
                "behavioral_levels": BehavioralEvaluationLevelEnum.choices,
                "educational_types": EducationalRecordTypeEnum.choices,
            },
        )

    def post(self, request, record_id):
        record = get_object_or_404(StudentDevelopmentRecordModel, id=record_id)

        record.title = request.POST.get("title")
        record.description = request.POST.get("description")

        record.category = request.POST.get("category")
        record.effect = request.POST.get("effect")
        record.level = request.POST.get("level")
        record.educational_type = request.POST.get("educational_type")

        record.save()

        messages.success(request, "تشویقی با موفقیت بروزرسانی شد.")
        return redirect("discipline:admin_reward_detail", record_id=record.id)


class AdminRewardDeleteView(AdminRequiredMixin, View):
    def post(self, request, record_id):
        record = get_object_or_404(StudentDevelopmentRecordModel, id=record_id)
        record.delete()
        messages.success(request, "تشویقی حذف شد.")
        return redirect("discipline:admin_reward_list")


class StudentRewardListView(LoginRequiredMixin, View):
    template_name = "student/reward_list.html"

    def get(self, request):
        student = request.user.student

        records = StudentDevelopmentRecordModel.objects.filter(
            student=student, effect="positive", is_deleted=False  # اگر سافت‌دلیت داری
        ).select_related("classroom", "recorder")

        return render(
            request,
            self.template_name,
            {
                "records": records,
                "student": student,
            },
        )
