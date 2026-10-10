from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import TemplateView

from apps.academic.models import ScheduleSessionModel
from apps.academic.services.active_year import get_active_year
from apps.account.enums import UserRoleEnum
from apps.attendance.models import StaffAttendanceModel, StudentAttendanceModel


class DashboardView(LoginRequiredMixin, TemplateView):
    template_name = "dashboard/dashboard.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        user = self.request.user

        # نقش کاربر
        if user.is_superuser:
            role = UserRoleEnum.ADMIN
        elif hasattr(user, "role"):
            role = user.role
        else:
            role = "unknown"

        context["role"] = role

        active_year = get_active_year(self.request)

        # -----------------------------
        # 🟦 داشبورد معلم
        # -----------------------------
        if role == UserRoleEnum.TEACHER:
            teacher = user.teacher
            context["teacher"] = teacher
            context["active_year"] = active_year

            # برنامه هفتگی معلم
            schedules = ScheduleSessionModel.objects.filter(
                teacher=teacher, classroom__academic_year=active_year
            ).select_related("classroom", "subject")
            context["sessions"] = schedules

            # 🔥 فقط غیبت‌های خود معلم (StaffAttendanceModel)
            teacher_absents = StaffAttendanceModel.objects.filter(
                teacher=teacher, status="absent"
            )

            context["total_absents"] = teacher_absents.count()

            context["absent_dates"] = [
                {
                    "date": rec.date,
                    "arrival": rec.arrival_time,
                    "departure": rec.departure_time,
                    "description": rec.description,
                }
                for rec in teacher_absents
            ]

        # -----------------------------
        # 🟩 داشبورد دانش‌آموز
        # -----------------------------
        elif role == UserRoleEnum.STUDENT:
            student = user.student
            context["student"] = student
            context["active_year"] = active_year

            # کلاس‌های دانش‌آموز
            classrooms = student.classrooms.filter(academic_year=active_year)
            context["classrooms"] = classrooms

            # برنامه هفتگی
            sessions = ScheduleSessionModel.objects.filter(
                classroom__in=classrooms
            ).select_related("subject", "teacher")
            context["sessions"] = sessions

            # 🔥 فقط غیبت‌های خود دانش‌آموز
            student_absents = StudentAttendanceModel.objects.filter(
                student=student, status="absent"
            ).select_related("session__schedule_session__subject")

            context["total_absents"] = student_absents.count()

            # غیبت‌ها بر اساس درس
            absents_by_subject = {}
            for rec in student_absents:
                subject = rec.session.schedule_session.subject.name
                absents_by_subject.setdefault(subject, 0)
                absents_by_subject[subject] += 1

            context["absents_by_subject"] = absents_by_subject

            # تاریخ‌های غیبت
            context["absent_dates"] = [
                {
                    "date": rec.session.date,
                    "subject": rec.session.schedule_session.subject.name,
                }
                for rec in student_absents
            ]

        return context
