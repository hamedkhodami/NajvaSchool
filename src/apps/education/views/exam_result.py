from django.contrib import messages
from django.shortcuts import get_object_or_404, redirect, render
from django.views import View

from apps.academic.models import ClassroomModel
from apps.academic.services.active_year import get_active_year
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
        return redirect("education:exam_list")


class TeacherClassListView(TeacherRequiredMixin, View):
    template_name = "education/exam_result/class_list.html"

    def get(self, request):
        teacher = request.user.teacher

        active_year = get_active_year(request)

        teacher_classrooms = ClassroomModel.objects.filter(
            schedule_sessions__teacher=teacher
        ).distinct()

        classrooms = teacher_classrooms.filter(academic_year=active_year)

        return render(request, self.template_name, {"classrooms": classrooms})


class TeacherClassExamResultView(TeacherRequiredMixin, View):
    template_name = "education/exam_result/class_exam_results.html"

    def get(self, request, classroom_id):
        teacher = request.user.teacher

        active_year = get_active_year(request)

        teacher_classrooms = ClassroomModel.objects.filter(
            schedule_sessions__teacher=teacher
        ).distinct()

        classroom = get_object_or_404(
            teacher_classrooms.filter(id=classroom_id, academic_year=active_year)
        )

        students = classroom.students.all()

        exams = ExamModel.objects.filter(classroom=classroom, teacher=teacher).order_by(
            "created_at"
        )

        table_rows = []

        for student in students:
            student_scores = []
            total_scores = []

            for exam in exams:
                result = ExamResultModel.objects.filter(
                    exam=exam, student=student
                ).first()

                if result:
                    student_scores.append(result.score)
                    total_scores.append(result.score)
                else:
                    student_scores.append(None)

            avg_score = sum(total_scores) / len(total_scores) if total_scores else None

            table_rows.append(
                {
                    "student": student,
                    "scores": student_scores,
                    "avg": avg_score,
                }
            )

        return render(
            request,
            self.template_name,
            {
                "classroom": classroom,
                "exams": exams,
                "table_rows": table_rows,
            },
        )


class StudentExamResultListView(View):
    template_name = "education/exam_result/student_exam_results.html"

    def get(self, request):
        student = request.user.student

        # سال تحصیلی فعال
        active_year = get_active_year(request)

        # کلاس‌های دانش‌آموز در سال فعال
        classrooms = ClassroomModel.objects.filter(
            students=student, academic_year=active_year
        )

        # امتحاناتی که دانش‌آموز در آن‌ها نتیجه دارد
        results = ExamResultModel.objects.filter(
            student=student, exam__classroom__in=classrooms
        ).select_related("exam", "exam__subject", "exam__teacher")

        return render(
            request,
            self.template_name,
            {
                "results": results,
                "active_year": active_year,
            },
        )
