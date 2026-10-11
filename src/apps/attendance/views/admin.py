from django.contrib import messages
from django.db.models import Q
from django.shortcuts import redirect, render
from django.views import View

from apps.academic.services.active_year import get_active_year
from apps.account.mixins import AdminRequiredMixin
from apps.attendance.enums import AttendanceStatusEnum, StaffAttendanceStatusEnum
from apps.attendance.forms import StaffAttendanceForm
from apps.attendance.models import StaffAttendanceModel, StudentAttendanceModel
from apps.core.templatetags.jalali import (
    gregorian_to_jalali,
    jalali_days_in_month,
    jalali_to_gregorian,
    today_gregorian,
)


class AdminAbsenceListView(AdminRequiredMixin, View):
    template_name = "attendance/admin/admin_absence_list.html"

    def get(self, request):
        active_year = get_active_year(request)

        # جستجو
        q = request.GET.get("q", "").strip()

        # فیلتر ماه و روز
        month = request.GET.get("month")
        day = request.GET.get("day")

        # دکمه امروز
        today = today_gregorian() if request.GET.get("today") == "1" else None

        # سال تحصیلی فعال (شمسی)
        j_start = gregorian_to_jalali(active_year.start_date)
        j_end = gregorian_to_jalali(active_year.end_date)

        start_year = j_start.year
        end_year = j_end.year

        # کوئری پایه
        absences = StudentAttendanceModel.objects.filter(
            status=AttendanceStatusEnum.ABSENT,
            session__schedule_session__classroom__academic_year=active_year,
        ).select_related(
            "student",
            "session",
            "session__schedule_session",
            "session__schedule_session__classroom",
        )

        # فیلتر جستجو
        if q:
            absences = absences.filter(
                Q(student__user__full_name__icontains=q)
                | Q(student__user__phone_number__icontains=q)
            )

        # فیلتر ماه + روز
        if month and day:
            month = int(month)
            day = int(day)

            # تعیین سال صحیح
            j_year = start_year if month >= 7 else end_year

            g_date = jalali_to_gregorian(j_year, month, day)
            absences = absences.filter(session__date=g_date)

        # فیلتر امروز
        if today:
            absences = absences.filter(session__date=today)

        # ساخت لیست روزهای ماه
        if month:
            month = int(month)
            j_year = start_year if month >= 7 else end_year
            total_days = jalali_days_in_month(j_year, month)
            days_list = list(range(1, total_days + 1))
        else:
            days_list = None

        # ماه‌های سال تحصیلی فعال
        months = [7, 8, 9, 10, 11, 12, 1, 2, 3, 4, 5, 6]

        return render(
            request,
            self.template_name,
            {
                "absences": absences,
                "months": months,
                "days_list": days_list,
                "month": month,
                "day": day,
                "q": q,
                "active_year": active_year,
            },
        )


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
            status=StaffAttendanceStatusEnum.ABSENT,
            teacher__schedule_sessions__classroom__academic_year=active_year,
        ).select_related("teacher")

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

        return render(
            request,
            self.template_name,
            {
                "absences": absences,
                "months": months,
                "days_list": days_list,
                "month": month,
                "day": day,
                "q": q,
                "active_year": active_year,
            },
        )


class AdminTeacherAbsenceCreateView(AdminRequiredMixin, View):
    template_name = "attendance/admin/admin_teacher_absence_create.html"

    def get(self, request):
        active_year = get_active_year(request)

        if not active_year:
            messages.error(request, "سال تحصیلی فعال یافت نشد.")
            return redirect("attendance:admin_teacher_absence_list")

        form = StaffAttendanceForm()
        return render(
            request, self.template_name, {"form": form, "active_year": active_year}
        )

    def post(self, request):
        active_year = get_active_year(request)

        if not active_year:
            messages.error(request, "سال تحصیلی فعال یافت نشد.")
            return redirect("attendance:admin_teacher_absence_list")

        form = StaffAttendanceForm(request.POST)

        if form.is_valid():
            obj = form.save(commit=False)

            # جلوگیری از ثبت غیبت خارج از سال تحصیلی
            if not (active_year.start_date <= obj.date <= active_year.end_date):
                form.add_error("date", "تاریخ انتخاب‌شده خارج از سال تحصیلی فعال است.")
                return render(request, self.template_name, {"form": form})

            obj.save()
            messages.success(request, "غیبت معلم با موفقیت ثبت شد.")
            return redirect("attendance:admin_teacher_absence_list")

        return render(request, self.template_name, {"form": form})
