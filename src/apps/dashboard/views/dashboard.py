from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import redirect
from django.views.generic import TemplateView

from apps.academic.models import ScheduleSessionModel
from apps.academic.services.active_year import get_active_year
from apps.account.enums import UserRoleEnum
from apps.attendance.models import StaffAttendanceModel, StudentAttendanceModel
from apps.notification.models import Notification


class DashboardView(LoginRequiredMixin, TemplateView):
    template_name = "dashboard/dashboard.html"

    def get(self, request, *args, **kwargs):

        has_unread_notifications = Notification.objects.filter(
            to_user=request.user,
            is_showing=True,
            is_read=False,
        ).exists()

        if has_unread_notifications:
            return redirect("notification:pending_notifications")

        return super().get(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        user = self.request.user

        # -------------------------
        # تعیین نقش کاربر
        # -------------------------
        if user.is_superuser:
            role = UserRoleEnum.ADMIN
        elif hasattr(user, "role"):
            role = user.role
        else:
            role = "unknown"

        context["role"] = role

        # -------------------------
        # تعداد اعلان‌های خوانده‌نشده
        # -------------------------
        context["unread_notifications_count"] = Notification.objects.filter(
            to_user=user,
            is_showing=True,
            is_read=False,
        ).count()

        # -------------------------
        # سال تحصیلی فعال
        # -------------------------
        active_year = get_active_year(self.request)
        context["active_year"] = active_year

        weekdays = [
            ("saturday", "شنبه"),
            ("sunday", "یکشنبه"),
            ("monday", "دوشنبه"),
            ("tuesday", "سه‌شنبه"),
            ("wednesday", "چهارشنبه"),
            ("thursday", "پنجشنبه"),
            ("friday", "جمعه"),
        ]

        # -------------------------
        # داشبورد معلم
        # -------------------------
        if role == UserRoleEnum.TEACHER:
            teacher = user.teacher
            context["teacher"] = teacher

            schedules = list(
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
                .order_by("session_number")
            )

            context["sessions"] = schedules

            schedule_days = []

            for value, label in weekdays:
                schedule_days.append(
                    {
                        "value": value,
                        "label": label,
                        "sessions": [
                            session for session in schedules if session.weekday == value
                        ],
                    }
                )

            context["schedule_days"] = schedule_days

            # تمام غیبت‌های معلم
            all_absents = StaffAttendanceModel.objects.filter(
                teacher=teacher,
                status=StaffAttendanceModel.Status.ABSENT,
            ).order_by("-date", "-created_at", "-pk")

            context["total_absents"] = all_absents.count()
            context["all_absents"] = all_absents

        # -------------------------
        # داشبورد دانش‌آموز
        # -------------------------
        elif role == UserRoleEnum.STUDENT:
            student = user.student
            context["student"] = student

            classrooms = student.classrooms.filter(
                academic_year=active_year
            ).select_related("academic_year")

            context["classrooms"] = classrooms

            schedules = list(
                ScheduleSessionModel.objects.filter(classroom__in=classrooms)
                .select_related(
                    "classroom",
                    "classroom__academic_year",
                    "subject",
                    "teacher",
                    "teacher__user",
                )
                .order_by("session_number")
            )

            context["sessions"] = schedules

            schedule_days = []

            for value, label in weekdays:
                schedule_days.append(
                    {
                        "value": value,
                        "label": label,
                        "sessions": [
                            session for session in schedules if session.weekday == value
                        ],
                    }
                )

            context["schedule_days"] = schedule_days

            # تمام رکوردهای غیبت دانش‌آموز
            all_absents = (
                StudentAttendanceModel.objects.filter(
                    student=student,
                    status=StudentAttendanceModel.Status.ABSENT,
                )
                .select_related(
                    "session",
                    "session__schedule_session",
                    "session__schedule_session__subject",
                )
                .order_by(
                    "-session__date",
                    "-created_at",
                    "-pk",
                )
            )

            context["total_absents"] = all_absents.count()

            absent_dates = []
            absents_by_subject = {}

            for record in all_absents:
                attendance_session = record.session
                schedule = attendance_session.schedule_session

                if schedule and schedule.subject:
                    subject_name = schedule.subject.name
                else:
                    subject_name = "درس نامشخص"

                absent_dates.append(
                    {
                        "id": record.pk,
                        "date": attendance_session.date,
                        "subject": subject_name,
                        "description": record.description,
                    }
                )

                absents_by_subject[subject_name] = (
                    absents_by_subject.get(subject_name, 0) + 1
                )

            context["absent_dates"] = absent_dates
            context["absents_by_subject"] = absents_by_subject

        return context
