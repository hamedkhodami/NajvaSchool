from django.contrib import messages
from django.db import transaction
from django.db.models import Count
from django.http import HttpResponseRedirect, JsonResponse
from django.shortcuts import get_object_or_404, render
from django.urls import reverse
from django.utils.decorators import method_decorator
from django.views import View
from django.views.decorators.cache import never_cache
from django.views.generic import TemplateView

from apps.academic.models import ScheduleSessionModel
from apps.academic.services.active_year import get_active_year
from apps.attendance.enums import AttendanceStatusEnum
from apps.attendance.models import AttendanceSessionModel, StudentAttendanceModel
from apps.core.pagination import paginate_queryset
from apps.core.templatetags.jalali import (
    gregorian_to_jalali,
    jalali_to_gregorian,
    today_gregorian,
)
from apps.notification.enums import NotificationTypeEnum
from apps.notification.utils import create_in_app_notification
from apps.student.models import StudentModel
from apps.teacher.mixins import TeacherOrAdminRequiredMixin


class TeacherAttendanceOverviewView(TeacherOrAdminRequiredMixin, View):
    template_name = "attendance/teacher/overview.html"

    WEEKDAYS = [
        ("saturday", "شنبه"),
        ("sunday", "یکشنبه"),
        ("monday", "دوشنبه"),
        ("tuesday", "سه‌شنبه"),
        ("wednesday", "چهارشنبه"),
        ("thursday", "پنجشنبه"),
        ("friday", "جمعه"),
    ]

    def get(self, request, *args, **kwargs):
        teacher = request.user.teacher
        active_year = get_active_year(request)

        schedules = list(
            ScheduleSessionModel.objects.filter(
                teacher=teacher,
                classroom__academic_year=active_year,
            )
            .select_related(
                "classroom",
                "classroom__academic_year",
                "subject",
            )
            .order_by("session_number")
        )

        schedule_days = []

        for value, label in self.WEEKDAYS:
            day_sessions = [
                session for session in schedules if session.weekday == value
            ]

            schedule_days.append(
                {
                    "value": value,
                    "label": label,
                    "sessions": day_sessions,
                    "session_count": len(day_sessions),
                }
            )

        context = {
            "schedules": schedules,
            "schedule_days": schedule_days,
            "active_year": active_year,
            "total_sessions": len(schedules),
            "has_sessions": bool(schedules),
            "active_days_count": sum(1 for day in schedule_days if day["sessions"]),
        }

        return render(request, self.template_name, context)


class TeacherAttendanceSessionView(TeacherOrAdminRequiredMixin, View):
    template_name = "attendance/teacher/session_detail.html"

    def get(self, request, schedule_id):
        teacher = request.user.teacher
        schedule = get_object_or_404(
            ScheduleSessionModel, id=schedule_id, teacher=teacher
        )

        date_j = request.GET.get("date")
        if date_j:
            try:
                g_date = jalali_to_gregorian(*map(int, date_j.split("-")))
            except Exception:
                g_date = today_gregorian()
        else:
            g_date = today_gregorian()

        attendance_session = AttendanceSessionModel.objects.filter(
            schedule_session=schedule, date=g_date
        ).first()

        students = schedule.classroom.students.select_related("user").all()

        attendance_map = {}
        if attendance_session:
            records = StudentAttendanceModel.objects.filter(
                session=attendance_session
            ).select_related("student__user")
            attendance_map = {r.student_id: r for r in records}

        notes = []

        if attendance_session:
            notes = list(
                attendance_session.teacher_notes.select_related("teacher").order_by(
                    "-created_at"
                )
            )

        latest_note = None

        previous_sessions = schedule.attendance_sessions.order_by("-date", "-id")

        for previous_session in previous_sessions:
            latest_note = (
                previous_session.teacher_notes.select_related("teacher")
                .order_by("-created_at")
                .first()
            )

            if latest_note:
                break

        return render(
            request,
            self.template_name,
            {
                "schedule": schedule,
                "date": g_date,
                "date_jalali": gregorian_to_jalali(g_date),
                "attendance_session": attendance_session,
                "students": students,
                "attendance_map": attendance_map,
                "notes": notes,
                "latest_note": latest_note,
            },
        )

    def post(self, request, schedule_id):
        teacher = request.user.teacher

        schedule = get_object_or_404(
            ScheduleSessionModel.objects.select_related("classroom"),
            id=schedule_id,
            teacher=teacher,
        )

        date_j = request.POST.get("date", "").strip()

        if not date_j:
            messages.error(request, "تاریخ جلسه مشخص نشده است.")
            return HttpResponseRedirect(request.path)

        try:
            date_parts = [int(part) for part in date_j.split("-")]
            if len(date_parts) != 3:
                raise ValueError
            g_date = jalali_to_gregorian(*date_parts)
        except (TypeError, ValueError):
            messages.error(request, "فرمت تاریخ نامعتبر است.")
            return HttpResponseRedirect(request.path)

        students = list(schedule.classroom.students.all())

        if not students:
            messages.error(request, "برای این کلاس دانش‌آموزی ثبت نشده است.")
            return HttpResponseRedirect(
                f"{reverse('attendance:teacher_session', args=[schedule.id])}?date={date_j}"
            )

        valid_statuses = {"present", "absent"}
        attendance_data = {}

        for student in students:
            status_value = request.POST.get(f"attendance_{student.pk}", "").strip()

            if status_value not in valid_statuses:
                messages.error(
                    request,
                    "وضعیت حضور و غیاب یکی از دانش‌آموزان انتخاب نشده یا نامعتبر است.",
                )
                return HttpResponseRedirect(
                    f"{reverse('attendance:teacher_session', args=[schedule.id])}?date={date_j}"
                )

            attendance_data[student.pk] = (
                AttendanceStatusEnum.PRESENT
                if status_value == "present"
                else AttendanceStatusEnum.ABSENT
            )

        note_text = request.POST.get("note", "").strip()

        with transaction.atomic():
            attendance_session, created = AttendanceSessionModel.objects.get_or_create(
                schedule_session=schedule,
                date=g_date,
                defaults={
                    "description": "",
                    "session_number": schedule.session_number,
                },
            )

            for student_id, status in attendance_data.items():

                previous_record = StudentAttendanceModel.objects.filter(
                    session=attendance_session,
                    student_id=student_id,
                ).first()

                was_absent = (
                    previous_record is not None
                    and previous_record.status == AttendanceStatusEnum.ABSENT
                )

                StudentAttendanceModel.objects.update_or_create(
                    session=attendance_session,
                    student_id=student_id,
                    defaults={"status": status},
                )

                # فقط اگر وضعیت جدید غیبت باشد و قبلاً غیبت ثبت نشده باشد
                if status == AttendanceStatusEnum.ABSENT and not was_absent:
                    student = next(s for s in students if s.pk == student_id)

                    create_in_app_notification(
                        to_user=student.user,
                        notification_type=NotificationTypeEnum.ATTENDANCE,
                        title="ثبت غیبت در کلاس",
                        description=(
                            f"برای شما در جلسه شماره "
                            f"{attendance_session.session_number} "
                            f"در تاریخ {g_date} غیبت ثبت شده است."
                        ),
                    )

            if note_text:
                attendance_session.teacher_notes.create(
                    teacher=teacher,
                    content=note_text,
                )

        messages.success(request, "حضور و غیاب با موفقیت ثبت شد.")

        return HttpResponseRedirect(
            f"{reverse('attendance:teacher_session', args=[schedule.id])}?date={date_j}"
        )


@method_decorator(never_cache, name="dispatch")
class TeacherToggleAttendanceView(TeacherOrAdminRequiredMixin, View):
    def post(self, request):
        session_id = request.POST.get("session_id")
        student_id = request.POST.get("student_id")
        status = request.POST.get("status", "absent")

        if not (session_id and student_id):
            return JsonResponse(
                {"ok": False, "error": "پارامترهای لازم ارسال نشده‌اند"},
                status=400,
            )

        if status not in {"present", "absent"}:
            return JsonResponse(
                {"ok": False, "error": "وضعیت ارسال‌شده معتبر نیست"},
                status=400,
            )

        try:
            attendance_session = AttendanceSessionModel.objects.select_related(
                "schedule_session",
                "schedule_session__teacher",
            ).get(id=session_id)
        except AttendanceSessionModel.DoesNotExist:
            return JsonResponse(
                {"ok": False, "error": "جلسه یافت نشد"},
                status=404,
            )

        if (
            not attendance_session.schedule_session
            or attendance_session.schedule_session.teacher.user_id != request.user.id
        ):
            return JsonResponse(
                {"ok": False, "error": "دسترسی ندارید"},
                status=403,
            )

        student = get_object_or_404(
            StudentModel,
            id=student_id,
            classrooms=attendance_session.schedule_session.classroom,
        )

        status_enum = (
            AttendanceStatusEnum.PRESENT
            if status == "present"
            else AttendanceStatusEnum.ABSENT
        )

        with transaction.atomic():
            previous_record = StudentAttendanceModel.objects.filter(
                session=attendance_session,
                student=student,
            ).first()

            was_absent = (
                previous_record is not None
                and previous_record.status == AttendanceStatusEnum.ABSENT
            )

            rec, created = StudentAttendanceModel.objects.update_or_create(
                session=attendance_session,
                student=student,
                defaults={"status": status_enum},
            )

            if status_enum == AttendanceStatusEnum.ABSENT and not was_absent:
                create_in_app_notification(
                    to_user=student.user,
                    notification_type=NotificationTypeEnum.ATTENDANCE,
                    title="ثبت غیبت در کلاس",
                    description=(
                        f"برای شما در جلسه شماره "
                        f"{attendance_session.session_number} "
                        f"غیبت ثبت شده است."
                    ),
                )

        return JsonResponse({"ok": True, "status": status_enum})


class TeacherAttendanceListsView(TeacherOrAdminRequiredMixin, TemplateView):
    template_name = "attendance/teacher/attendance_lists.html"

    def dispatch(self, request, *args, **kwargs):
        self.schedule = get_object_or_404(
            ScheduleSessionModel.objects.select_related(
                "teacher",
                "classroom",
                "subject",
            ),
            pk=kwargs["schedule_id"],
            teacher__user=request.user,
        )
        return super().dispatch(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        attendance_lists = (
            AttendanceSessionModel.objects.filter(schedule_session=self.schedule)
            .annotate(student_count=Count("student_attendances"))
            .order_by("-date", "-session_number", "-pk")
        )

        pagination = paginate_queryset(
            request=self.request,
            queryset=attendance_lists,
            per_page=10,
        )

        context.update(
            {
                "schedule": self.schedule,
                "attendance_lists": pagination["object_list"],
                "paginator": pagination["paginator"],
                "page_obj": pagination["page_obj"],
                "is_paginated": pagination["is_paginated"],
                "total_lists": pagination["paginator"].count,
            }
        )

        return context


class TeacherAttendanceListDetailView(TeacherOrAdminRequiredMixin, TemplateView):
    template_name = "attendance/teacher/attendance_list_detail.html"

    def dispatch(self, request, *args, **kwargs):
        self.schedule = get_object_or_404(
            ScheduleSessionModel.objects.select_related(
                "teacher",
                "classroom",
                "subject",
            ),
            pk=kwargs["schedule_id"],
            teacher__user=request.user,
        )

        self.attendance_session = get_object_or_404(
            AttendanceSessionModel.objects.select_related(
                "schedule_session",
            ),
            pk=kwargs["attendance_session_id"],
            schedule_session=self.schedule,
        )

        return super().dispatch(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        attendances = (
            StudentAttendanceModel.objects.filter(session=self.attendance_session)
            .select_related(
                "student",
                "student__user",
            )
            .order_by(
                "student__user__last_name",
                "student__user__first_name",
            )
        )

        context["schedule"] = self.schedule
        context["attendance_session"] = self.attendance_session
        context["attendances"] = attendances
        context["total_students"] = attendances.count()

        context["present_count"] = attendances.filter(
            status=StudentAttendanceModel.Status.PRESENT
        ).count()

        context["absent_count"] = attendances.filter(
            status=StudentAttendanceModel.Status.ABSENT
        ).count()

        return context
