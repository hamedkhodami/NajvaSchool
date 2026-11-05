from django.contrib import messages
from django.shortcuts import get_object_or_404, redirect, render
from django.utils.decorators import method_decorator
from django.views import View
from django.views.decorators.cache import never_cache

from apps.academic.models import SubjectModel
from apps.academic.services.active_year import get_active_year
from apps.core.pagination import paginate_queryset
from apps.education.forms import ExamCreateForm, ExamUpdateForm
from apps.education.models import ExamModel
from apps.teacher.mixins import TeacherOrAdminRequiredMixin, TeacherRequiredMixin


class TeacherExamCreateView(TeacherRequiredMixin, View):
    template_name = "education/exam/teacher_exam_create.html"

    def get(self, request):
        teacher = request.user.teacher
        active_year = get_active_year(request)

        form = ExamCreateForm(teacher=teacher, active_year=active_year)
        return render(request, self.template_name, {"form": form})

    def post(self, request):
        teacher = request.user.teacher
        active_year = get_active_year(request)

        form = ExamCreateForm(
            request.POST, request.FILES, teacher=teacher, active_year=active_year
        )

        if form.is_valid():
            exam = form.save(commit=False)
            exam.teacher = teacher
            exam.save()

            messages.success(request, "امتحان با موفقیت ثبت شد.")
            return redirect("education:exam_list")

        return render(request, self.template_name, {"form": form})


class TeacherExamListView(TeacherRequiredMixin, View):
    template_name = "education/exam/teacher_exam_list.html"

    def get(self, request):
        active_year = get_active_year(request)
        teacher = request.user.teacher

        exams = (
            ExamModel.objects.filter(
                teacher=teacher,
                classroom__academic_year=active_year,
            )
            .select_related("classroom", "subject")
            .order_by("-id")
        )

        pagination = paginate_queryset(request, exams, per_page=10)

        return render(
            request,
            self.template_name,
            {
                "exams": pagination["object_list"],
                "paginator": pagination["paginator"],
                "page_obj": pagination["page_obj"],
                "is_paginated": pagination["is_paginated"],
            },
        )


class TeacherExamDetailView(TeacherRequiredMixin, View):
    template_name = "education/exam/teacher_exam_detail.html"

    def get(self, request, exam_id):
        teacher = request.user.teacher
        exam = get_object_or_404(ExamModel, id=exam_id, teacher=teacher)
        return render(request, self.template_name, {"exam": exam})


@method_decorator(never_cache, name="dispatch")
class TeacherExamUpdateView(TeacherRequiredMixin, View):
    template_name = "education/exam/teacher_exam_edit.html"

    def get(self, request, exam_id):
        teacher = request.user.teacher
        active_year = get_active_year(request)

        exam = get_object_or_404(ExamModel, id=exam_id, teacher=teacher)
        form = ExamUpdateForm(instance=exam, teacher=teacher, active_year=active_year)

        return render(request, self.template_name, {"form": form, "exam": exam})

    def post(self, request, exam_id):
        teacher = request.user.teacher
        active_year = get_active_year(request)

        exam = get_object_or_404(ExamModel, id=exam_id, teacher=teacher)

        form = ExamUpdateForm(
            request.POST,
            request.FILES,
            instance=exam,
            teacher=teacher,
            active_year=active_year,
        )

        if form.is_valid():
            form.save()
            messages.success(request, "امتحان با موفقیت ویرایش شد.")
            return redirect("education:exam_list")

        return render(request, self.template_name, {"form": form, "exam": exam})


class QuestionBankListView(TeacherOrAdminRequiredMixin, View):
    template_name = "education/exam/question_bank_list.html"

    def get(self, request):
        exams = (
            ExamModel.objects.filter(file__isnull=False)
            .exclude(file="")
            .select_related(
                "teacher",
                "teacher__user",
                "subject",
                "classroom",
                "classroom__academic_year",
            )
            .order_by("-id")
        )

        subject_id = request.GET.get("subject")

        if subject_id:
            exams = exams.filter(subject_id=subject_id)

        subjects = SubjectModel.objects.all()

        pagination = paginate_queryset(request, exams, per_page=10)

        return render(
            request,
            self.template_name,
            {
                "exams": pagination["object_list"],
                "paginator": pagination["paginator"],
                "page_obj": pagination["page_obj"],
                "is_paginated": pagination["is_paginated"],
                "subjects": subjects,
                "selected_subject": subject_id,
            },
        )
