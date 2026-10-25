from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import TemplateView

from apps.academic.models import ScheduleSessionModel
from apps.academic.services.active_year import get_active_year
from apps.account.enums import UserRoleEnum
from apps.attendance.enums import StaffAttendanceStatusEnum
from apps.attendance.models import StaffAttendanceModel, StudentAttendanceModel


class DashboardView(LoginRequiredMixin, TemplateView):
    template_name = "dashboard/dashboard.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        user = self.request.user

        # -----------------------------
        # نقش کاربر
        # -----------------------------
        if user.is_superuser:
            role = UserRoleEnum.ADMIN
        elif hasattr(user, "role"):
            role = user.role
        else:
            role = "unknown"

        context["role"] = role

        # اعلان‌ها: مقدار موقت تا زمان اتصال مدل اعلان
        context["unread_notifications_count"] = 0

        active_year = get_active_year(self.request)
        context["active_year"] = active_year

        # روزهای هفته
        weekdays = [
            ("saturday", "شنبه"),
            ("sunday", "یکشنبه"),
            ("monday", "دوشنبه"),
            ("tuesday", "سه‌شنبه"),
            ("wednesday", "چهارشنبه"),
            ("thursday", "پنجشنبه"),
            ("friday", "جمعه"),
        ]

        # -----------------------------
        # داشبورد معلم
        # -----------------------------
        if role == UserRoleEnum.TEACHER:
            teacher = user.teacher
            context["teacher"] = teacher

            schedules = (
                ScheduleSessionModel.objects.filter(
                    teacher=teacher,
                    classroom__academic_year=active_year,
                )
                .select_related(
                    "classroom",
                    "classroom__academic_year",
                    "subject",
                    "teacher",
                    "teacher__user",
                )
                .order_by(
                    "session_number",
                )
            )

            context["sessions"] = schedules

            # برنامه هفتگی معلم
            schedule_days = []

            for value, label in weekdays:
                day_sessions = [
                    session for session in schedules if session.weekday == value
                ]

                schedule_days.append(
                    {
                        "value": value,
                        "label": label,
                        "sessions": day_sessions,
                    }
                )

            context["schedule_days"] = schedule_days

            # غیبت‌های معلم
            teacher_absents = StaffAttendanceModel.objects.filter(
                teacher=teacher,
                status=StaffAttendanceStatusEnum.ABSENT,
            ).order_by("-date")

            context["total_absents"] = teacher_absents.count()
            context["recent_absents"] = teacher_absents[:3]

        # -----------------------------
        # داشبورد دانش‌آموز
        # -----------------------------
        elif role == UserRoleEnum.STUDENT:
            student = user.student
            context["student"] = student

            # کلاس‌های دانش‌آموز در سال تحصیلی فعال
            classrooms = student.classrooms.filter(
                academic_year=active_year,
            ).select_related(
                "academic_year",
            )

            context["classrooms"] = classrooms

            # برنامه هفتگی دانش‌آموز
            sessions = (
                ScheduleSessionModel.objects.filter(
                    classroom__in=classrooms,
                )
                .select_related(
                    "classroom",
                    "classroom__academic_year",
                    "subject",
                    "teacher",
                    "teacher__user",
                )
                .order_by(
                    "session_number",
                )
            )

            context["sessions"] = sessions

            # ساخت برنامه روزانه، مشابه داشبورد معلم
            schedule_days = []

            for value, label in weekdays:
                day_sessions = [
                    session for session in sessions if session.weekday == value
                ]

                schedule_days.append(
                    {
                        "value": value,
                        "label": label,
                        "sessions": day_sessions,
                    }
                )

            context["schedule_days"] = schedule_days

            # غیبت‌های دانش‌آموز
            student_absents = (
                StudentAttendanceModel.objects.filter(
                    student=student,
                    status="absent",
                )
                .select_related(
                    "session",
                    "session__schedule_session",
                    "session__schedule_session__subject",
                )
                .order_by(
                    "-session__date",
                )
            )

            context["total_absents"] = student_absents.count()

            # تعداد غیبت‌ها بر اساس درس
            absents_by_subject = {}

            for record in student_absents:
                subject = record.session.schedule_session.subject.name

                absents_by_subject.setdefault(subject, 0)
                absents_by_subject[subject] += 1

            context["absents_by_subject"] = absents_by_subject

            # تاریخ‌های غیبت
            context["absent_dates"] = [
                {
                    "date": record.session.date,
                    "subject": record.session.schedule_session.subject.name,
                }
                for record in student_absents
            ]

        return context
