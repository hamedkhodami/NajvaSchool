from django.contrib import messages
from django.db.models import Q
from django.shortcuts import redirect, render
from django.utils import timezone
from django.views import View

from apps.academic.services.active_year import get_active_year
from apps.account.mixins import AdminRequiredMixin
from apps.attendance.enums import AttendanceStatusEnum, StaffAttendanceStatusEnum
from apps.attendance.forms import StaffAttendanceForm
from apps.attendance.models import StaffAttendanceModel, StudentAttendanceModel
from apps.core.pagination import paginate_queryset
from apps.core.templatetags.jalali import (
    gregorian_to_jalali,
    jalali_days_in_month,
    jalali_to_gregorian,
    today_gregorian,
)
from apps.notification.enums import NotificationTypeEnum
from apps.notification.utils import create_in_app_notification


class AdminAbsenceListView(AdminRequiredMixin, View):
    template_name = "attendance/admin/admin_absence_list.html"

    def get(self, request):
        active_year = get_active_year(request)

        q = request.GET.get("q", "").strip()
        month = request.GET.get("month")
        day = request.GET.get("day")

        today = today_gregorian() if request.GET.get("today") == "1" else None

        j_start = gregorian_to_jalali(active_year.start_date)
        j_end = gregorian_to_jalali(active_year.end_date)

        start_year = j_start.year
        end_year = j_end.year

        absences = StudentAttendanceModel.objects.filter(
            status=AttendanceStatusEnum.ABSENT,
            session__schedule_session__classroom__academic_year=active_year,
        ).select_related(
            "student",
            "session",
            "session__schedule_session",
            "session__schedule_session__classroom",
        )

        if q:
            absences = absences.filter(
                Q(student__user__full_name__icontains=q)
                | Q(student__user__phone_number__icontains=q)
            )

        if month and day:
            month = int(month)
            day = int(day)

            j_year = start_year if month >= 7 else end_year
            g_date = jalali_to_gregorian(j_year, month, day)

            absences = absences.filter(session__date=g_date)

        if today:
            absences = absences.filter(session__date=today)

        if month:
            month = int(month)
            j_year = start_year if month >= 7 else end_year
            total_days = jalali_days_in_month(j_year, month)
            days_list = list(range(1, total_days + 1))
        else:
            days_list = None

        months = [7, 8, 9, 10, 11, 12, 1, 2, 3, 4, 5, 6]

        pagination = paginate_queryset(
            request=request,
            queryset=absences,
            per_page=10,
        )

        context = {
            "absences": pagination["object_list"],
            "paginator": pagination["paginator"],
            "page_obj": pagination["page_obj"],
            "is_paginated": pagination["is_paginated"],
            "months": months,
            "days_list": days_list,
            "month": month,
            "day": day,
            "q": q,
            "active_year": active_year,
        }

        return render(request, self.template_name, context)


class AdminTeacherAbsenceListView(AdminRequiredMixin, View):
    template_name = "attendance/admin/admin_teacher_absence_list.html"

    def get(self, request):
        active_year = get_active_year(request)

        q = request.GET.get("q", "").strip()
        month = request.GET.get("month")
        day = request.GET.get("day")

        today = today_gregorian() if request.GET.get("today") == "1" else None

        j_start = gregorian_to_jalali(active_year.start_date)
        j_end = gregorian_to_jalali(active_year.end_date)

        start_year = j_start.year
        end_year = j_end.year

        absences = StaffAttendanceModel.objects.filter(
            status=StaffAttendanceStatusEnum.ABSENT
        ).select_related(
            "teacher",
            "teacher__user",
        )

        if q:
            absences = absences.filter(
                Q(teacher__user__full_name__icontains=q)
                | Q(teacher__user__phone_number__icontains=q)
            )

        if month and day:
            month = int(month)
            day = int(day)

            j_year = start_year if month >= 7 else end_year
            g_date = jalali_to_gregorian(j_year, month, day)

            absences = absences.filter(date=g_date)

        if today:
            absences = absences.filter(date=today)

        if month:
            month = int(month)
            j_year = start_year if month >= 7 else end_year
            total_days = jalali_days_in_month(j_year, month)
            days_list = list(range(1, total_days + 1))
        else:
            days_list = None

        months = [7, 8, 9, 10, 11, 12, 1, 2, 3, 4, 5, 6]

        pagination = paginate_queryset(
            request=request,
            queryset=absences,
            per_page=10,
        )

        context = {
            "absences": pagination["object_list"],
            "paginator": pagination["paginator"],
            "page_obj": pagination["page_obj"],
            "is_paginated": pagination["is_paginated"],
            "months": months,
            "days_list": days_list,
            "month": month,
            "day": day,
            "q": q,
            "active_year": active_year,
        }

        return render(request, self.template_name, context)


class AdminTeacherAbsenceCreateView(AdminRequiredMixin, View):
    template_name = "attendance/admin/admin_teacher_absence_create.html"

    def get(self, request):
        active_year = get_active_year(request)

        if not active_year:
            messages.error(request, "سال تحصیلی فعال یافت نشد.")
            return redirect("attendance:admin_teacher_absence_list")

        form = StaffAttendanceForm()

        return render(
            request,
            self.template_name,
            {
                "form": form,
                "active_year": active_year,
            },
        )

    def post(self, request):
        active_year = get_active_year(request)

        if not active_year:
            messages.error(request, "سال تحصیلی فعال یافت نشد.")
            return redirect("attendance:admin_teacher_absence_list")

        form = StaffAttendanceForm(request.POST)

        if not form.is_valid():
            return render(
                request,
                self.template_name,
                {
                    "form": form,
                    "active_year": active_year,
                },
            )

        today = timezone.localdate()

        # بررسی قرار داشتن تاریخ امروز در سال تحصیلی فعال
        if not (active_year.start_date <= today <= active_year.end_date):
            messages.error(
                request,
                "تاریخ امروز خارج از محدوده سال تحصیلی فعال است.",
            )
            return render(
                request,
                self.template_name,
                {
                    "form": form,
                    "active_year": active_year,
                },
            )

        teacher = form.cleaned_data["teacher"]
        status = form.cleaned_data["status"]
        description = form.cleaned_data["description"]

        # بررسی وضعیت قبلی معلم
        previous_record = StaffAttendanceModel.objects.filter(
            teacher=teacher,
            date=today,
        ).first()

        was_absent = (
            previous_record is not None
            and previous_record.status == StaffAttendanceStatusEnum.ABSENT
        )

        # ثبت یا به‌روزرسانی حضور و غیاب
        obj, created = StaffAttendanceModel.objects.update_or_create(
            teacher=teacher,
            date=today,
            defaults={
                "academic_year": active_year,
                "status": status,
                "description": description,
            },
        )

        is_absent = status == StaffAttendanceStatusEnum.ABSENT

        # ارسال اعلان در صورت ثبت غیبت جدید
        if is_absent and not was_absent:
            create_in_app_notification(
                to_user=teacher.user,
                notification_type=NotificationTypeEnum.ATTENDANCE,
                title="ثبت غیبت برای شما",
                description=(
                    f"غیبت شما در تاریخ {today} توسط مدیریت مدرسه ثبت شد."
                    + (f"\nتوضیحات: {description}" if description else "")
                ),
            )

        messages.success(
            request,
            (
                "غیبت معلم با موفقیت ثبت شد."
                if created
                else "وضعیت حضور/غیبت معلم برای امروز به‌روزرسانی شد."
            ),
        )

        return redirect("attendance:admin_teacher_absence_list")
