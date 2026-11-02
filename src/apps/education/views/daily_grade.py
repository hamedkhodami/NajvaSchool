from django.contrib import messages
from django.shortcuts import get_object_or_404, redirect, render
from django.views import View

from apps.academic.models import ClassroomModel, SubjectModel
from apps.academic.services.active_year import get_active_year
from apps.education.models import DailyGradeModel
from apps.notification.enums import NotificationTypeEnum
from apps.notification.utils import create_in_app_notification


class TeacherDailyGradeClassListView(View):
    template_name = "education/daily_grade/class_list.html"

    def get(self, request):
        teacher = request.user.teacher
        active_year = get_active_year(request)

        classrooms = ClassroomModel.objects.filter(
            academic_year=active_year, schedule_sessions__teacher=teacher
        ).distinct()

        return render(request, self.template_name, {"classrooms": classrooms})


class TeacherDailyGradeCreateView(View):
    template_name = "education/daily_grade/create.html"

    def get(self, request, classroom_id):
        teacher = request.user.teacher
        active_year = get_active_year(request)

        classroom = get_object_or_404(
            ClassroomModel.objects.filter(
                id=classroom_id,
                academic_year=active_year,
                schedule_sessions__teacher=teacher,
            ).distinct()
        )

        students = classroom.students.all()

        subjects = SubjectModel.objects.filter(
            schedule_sessions__teacher=teacher,
            schedule_sessions__classroom=classroom,
        ).distinct()

        return render(
            request,
            self.template_name,
            {
                "classroom": classroom,
                "students": students,
                "subjects": subjects,
            },
        )

    def post(self, request, classroom_id):
        teacher = request.user.teacher
        active_year = get_active_year(request)

        classroom = get_object_or_404(
            ClassroomModel.objects.filter(
                id=classroom_id,
                academic_year=active_year,
                schedule_sessions__teacher=teacher,
            ).distinct()
        )

        subject_id = request.POST.get("subject")
        title = request.POST.get("title")

        subject = get_object_or_404(
            SubjectModel,
            id=subject_id,
            schedule_sessions__teacher=teacher,
            schedule_sessions__classroom=classroom,
        )

        created_count = 0

        for key, value in request.POST.items():
            if key.startswith("score_") and value.strip():

                student_id = key.replace("score_", "")

                student = get_object_or_404(
                    classroom.students.select_related("user"),
                    id=student_id,
                )

                daily_grade = DailyGradeModel.objects.create(
                    student=student,
                    teacher=teacher,
                    classroom=classroom,
                    subject=subject,
                    title=title,
                    score=value,
                )

                # ارسال اعلان بعد از ثبت موفق نمره
                create_in_app_notification(
                    to_user=student.user,
                    notification_type=NotificationTypeEnum.EDUCATIONAL,
                    title="ثبت نمره روزانه جدید",
                    description=(
                        f"معلم شما یک نمره جدید برایتان ثبت کرده است.\n"
                        f"درس: {subject}\n"
                        f"عنوان: {title}\n"
                        f"نمره: {daily_grade.score}"
                    ),
                )

                created_count += 1

        messages.success(
            request,
            f"نمرات {created_count} دانش‌آموز با موفقیت ثبت شدند.",
        )

        return redirect("education:teacher_daily_grade_class_list")


class TeacherDailyGradeListView(View):
    template_name = "education/daily_grade/list.html"

    def get(self, request, classroom_id):
        teacher = request.user.teacher
        active_year = get_active_year(request)

        classroom = get_object_or_404(
            ClassroomModel.objects.filter(
                id=classroom_id,
                academic_year=active_year,
                schedule_sessions__teacher=teacher,
            ).distinct()
        )

        students = classroom.students.all()

        # تمام نمرات روزانه این کلاس توسط این معلم
        grades = (
            DailyGradeModel.objects.filter(classroom=classroom, teacher=teacher)
            .select_related("student", "subject")
            .order_by("created_at")
        )

        # ساخت جدول داینامیک
        table_rows = []

        for student in students:
            student_grades = grades.filter(student=student)

            scores = [g.score for g in student_grades]
            avg_score = sum(scores) / len(scores) if scores else None

            table_rows.append(
                {
                    "student": student,
                    "grades": student_grades,
                    "avg": avg_score,
                }
            )

        return render(
            request,
            self.template_name,
            {
                "classroom": classroom,
                "table_rows": table_rows,
            },
        )


class StudentDailyGradeListView(View):
    template_name = "education/daily_grade/student_list.html"

    def get(self, request):
        student = request.user.student
        active_year = get_active_year(request)

        # کلاس‌های دانش‌آموز در سال فعال
        classrooms = ClassroomModel.objects.filter(
            students=student, academic_year=active_year
        )

        # نمرات روزانه دانش‌آموز در سال فعال
        grades = (
            DailyGradeModel.objects.filter(student=student, classroom__in=classrooms)
            .select_related("subject", "teacher", "classroom")
            .order_by("-created_at")
        )

        # میانگین کل نمرات
        scores = [g.score for g in grades]
        avg_score = sum(scores) / len(scores) if scores else None

        return render(
            request,
            self.template_name,
            {
                "grades": grades,
                "avg_score": avg_score,
                "active_year": active_year,
            },
        )
