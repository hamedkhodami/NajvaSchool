from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.db import transaction
from django.http import HttpResponseRedirect, JsonResponse
from django.shortcuts import get_object_or_404, render
from django.urls import reverse
from django.views import View

from apps.academic.models import ScheduleSessionModel
from apps.academic.services.active_year import get_active_year
from apps.attendance.enums import AttendanceStatusEnum
from apps.attendance.models import AttendanceSessionModel, StudentAttendanceModel
from apps.core.templatetags.jalali import (
    gregorian_to_jalali,
    jalali_to_gregorian,
    today_gregorian,
)


class TeacherAttendanceOverviewView(LoginRequiredMixin, View):
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


class TeacherAttendanceSessionView(LoginRequiredMixin, View):
    template_name = "attendance/teacher/session_detail.html"

    def get(self, request, schedule_id):
        teacher = request.user.teacher
        schedule = get_object_or_404(
            ScheduleSessionModel, id=schedule_id, teacher=teacher
        )

        # تاریخ مورد نظر از پارامتر می‌آید یا امروز
        date_j = request.GET.get("date")  # انتظار: "1405-07-10" یا None
        if date_j:
            try:
                # تبدیل به تاریخ میلادی
                g_date = jalali_to_gregorian(*map(int, date_j.split("-")))
            except Exception:
                g_date = today_gregorian()
        else:
            g_date = today_gregorian()

        # جلسه حضور و غیاب مربوط به این schedule و تاریخ (اگر وجود نداشت، نمایش می‌دهیم و اجازهٔ ایجاد می‌دهیم)
        attendance_session = AttendanceSessionModel.objects.filter(
            schedule_session=schedule, date=g_date
        ).first()

        # لیست دانش‌آموزان کلاس (از classroom موجود در schedule)
        students = schedule.classroom.students.select_related("user").all()

        # وضعیت‌های ثبت‌شده برای این جلسه (اگر وجود دارد)
        attendance_map = {}
        if attendance_session:
            records = StudentAttendanceModel.objects.filter(
                session=attendance_session
            ).select_related("student__user")
            attendance_map = {r.student_id: r for r in records}

        # یادداشت‌های مرتبط با این attendance_session (فرض: TeacherNoteModel)
        notes = []
        if attendance_session:
            notes = (
                attendance_session.teacher_notes.select_related("teacher")
                .order_by("-created_at")
                .all()
            )

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
            },
        )

    def post(self, request, schedule_id):
        teacher = request.user.teacher
        schedule = get_object_or_404(
            ScheduleSessionModel, id=schedule_id, teacher=teacher
        )

        # تاریخ از فرم (باید فرمت شمسی دریافت شود)
        date_j = request.POST.get("date")  # مثال: "1405-07-10"
        if not date_j:
            messages.error(request, "تاریخ جلسه مشخص نشده است.")
            return HttpResponseRedirect(request.path)

        try:
            g_date = jalali_to_gregorian(*map(int, date_j.split("-")))
        except Exception:
            messages.error(request, "فرمت تاریخ نامعتبر است.")
            return HttpResponseRedirect(request.path)

        last_session = (
            AttendanceSessionModel.objects.filter(schedule_session=schedule)
            .order_by("-session_number")
            .first()
        )

        next_number = (last_session.session_number + 1) if last_session else 1

        attendance_session, created = AttendanceSessionModel.objects.get_or_create(
            schedule_session=schedule,
            date=g_date,
            defaults={
                "description": "",
                "session_number": next_number,
            },
        )

        # ثبت حضور/غیاب: انتظار داریم فرم یک مجموعه با کلید attendance_<student_id> داشته باشد
        # مقدار "present" یا "absent" یا خالی
        student_ids = request.POST.getlist("student_id")  # لیست idها (ترتیبی)
        # یا می‌توانیم از همهٔ دانش‌آموزان کلاس استفاده کنیم و برای هر کدوم وضعیت را بخوانیم
        with transaction.atomic():
            for sid in student_ids:
                status_val = request.POST.get(f"attendance_{sid}", "absent")
                # مقداردهی به enum
                status = (
                    AttendanceStatusEnum.PRESENT
                    if status_val == "present"
                    else AttendanceStatusEnum.ABSENT
                )

                # ایجاد یا بروزرسانی رکورد
                StudentAttendanceModel.objects.update_or_create(
                    session=attendance_session,
                    student_id=sid,
                    defaults={
                        "status": status,
                    },
                )

            # ثبت یادداشت (اختیاری)
            note_text = request.POST.get("note", "").strip()
            if note_text:
                # فرض: AttendanceSessionModel دارای related_name="teacher_notes" به TeacherNoteModel است
                attendance_session.teacher_notes.create(
                    teacher=teacher, content=note_text
                )

        messages.success(request, "حضور و غیاب با موفقیت ثبت شد.")
        # بازگشت به همان صفحه با تاریخ و schedule
        return HttpResponseRedirect(
            f"{reverse('attendance:teacher_session', args=[schedule.id])}?date={date_j}"
        )


class TeacherToggleAttendanceView(LoginRequiredMixin, View):
    def post(self, request):
        session_id = request.POST.get("session_id")
        student_id = request.POST.get("student_id")
        status = request.POST.get("status", "absent")

        if not (session_id and student_id):
            return JsonResponse(
                {"ok": False, "error": "پارامترهای لازم ارسال نشده‌اند"}, status=400
            )

        try:
            attendance_session = AttendanceSessionModel.objects.get(id=session_id)
        except AttendanceSessionModel.DoesNotExist:
            return JsonResponse({"ok": False, "error": "جلسه یافت نشد"}, status=404)

        if attendance_session.schedule_session.teacher.user != request.user:
            return JsonResponse({"ok": False, "error": "دسترسی ندارید"}, status=403)

        status_enum = (
            AttendanceStatusEnum.PRESENT
            if status == "present"
            else AttendanceStatusEnum.ABSENT
        )

        with transaction.atomic():
            rec, created = StudentAttendanceModel.objects.update_or_create(
                session=attendance_session,
                student_id=student_id,
                defaults={"status": status_enum},
            )

        return JsonResponse({"ok": True, "status": status_enum})
