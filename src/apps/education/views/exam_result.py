from django.contrib import messages
from django.shortcuts import get_object_or_404, redirect, render
from django.views import View

from apps.education.models import ExamModel, ExamResultModel
from apps.teacher.mixins import TeacherRequiredMixin


class TeacherExamResultView(TeacherRequiredMixin, View):
    template_name = "education/exam_result/teacher_exam_results.html"

    def get(self, request, exam_id):
        teacher = request.user.teacher
        exam = get_object_or_404(ExamModel, id=exam_id, teacher=teacher)

        students = exam.classroom.students.all()

        results_map = {
            r.student_id: r for r in ExamResultModel.objects.filter(exam=exam)
        }

        for s in students:
            s.exam_result = results_map.get(s.id)

        return render(
            request,
            self.template_name,
            {
                "exam": exam,
                "students": students,
            },
        )

    def post(self, request, exam_id):
        teacher = request.user.teacher
        exam = get_object_or_404(ExamModel, id=exam_id, teacher=teacher)

        students = exam.classroom.students.all()

        for student in students:
            score = request.POST.get(f"score_{student.id}")
            description = request.POST.get(f"desc_{student.id}")

            if score:
                ExamResultModel.objects.update_or_create(
                    exam=exam,
                    student=student,
                    defaults={
                        "score": score,
                        "description": description,
                    },
                )

        messages.success(request, "نمرات با موفقیت ثبت شدند.")
        return redirect("education:exam_list", exam_id=exam.id)
