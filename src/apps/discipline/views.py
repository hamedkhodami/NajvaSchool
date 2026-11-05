from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import get_object_or_404, redirect, render
from django.views import View

from apps.academic.models import ClassroomModel
from apps.academic.services.active_year import get_active_year
from apps.account.mixins import AdminRequiredMixin
from apps.core.pagination import paginate_queryset
from apps.discipline.enums import (
    BehavioralEvaluationLevelEnum,
    DisciplineEffectEnum,
    EducationalRecordTypeEnum,
    StudentRecordCategoryEnum,
)
from apps.discipline.models import StudentDevelopmentRecordModel
from apps.notification.enums import NotificationTypeEnum
from apps.notification.utils import create_in_app_notification


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
            return redirect(
                "discipline:admin_reward_create",
                classroom_id=classroom.id,
            )

        selected_students = students.filter(id__in=selected_ids)

        for student in selected_students:
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

            create_in_app_notification(
                to_user=student.user,
                notification_type=NotificationTypeEnum.DISCIPLINE,
                title="ثبت مورد جدید برای شما",
                description=(
                    f"یک مورد جدید با عنوان «{title}» برای شما ثبت شده است."
                    + (f"\nتوضیحات: {description}" if description else "")
                ),
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

        pagination = paginate_queryset(
            request=request,
            queryset=records,
            per_page=10,
        )

        context = {
            "active_year": active_year,
            "records": pagination["object_list"],
            "paginator": pagination["paginator"],
            "page_obj": pagination["page_obj"],
            "is_paginated": pagination["is_paginated"],
        }

        return render(request, self.template_name, context)


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

        pagination = paginate_queryset(
            request=request,
            queryset=records,
            per_page=10,
        )

        context = {
            "student": student,
            "records": pagination["object_list"],
            "paginator": pagination["paginator"],
            "page_obj": pagination["page_obj"],
            "is_paginated": pagination["is_paginated"],
        }

        return render(request, self.template_name, context)
