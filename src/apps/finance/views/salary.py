from decimal import Decimal, InvalidOperation
import json

from django.contrib import messages
from django.db.models import Q, Sum
from django.http import HttpResponse, HttpResponseBadRequest
from django.shortcuts import get_object_or_404, redirect, render
from django.views import View
from openpyxl import Workbook
from openpyxl.styles import Alignment, Border, Font, PatternFill, Side

from apps.academic.models import AcademicYearModel
from apps.academic.services.active_year import get_active_year
from apps.account.mixins import AdminRequiredMixin
from apps.finance.forms import (
    SalaryPaymentCreateForm,
    StaffSalaryCreateForm,
    StaffSalaryUpdateForm,
)
from apps.finance.models import StaffSalaryModel
from apps.notification.enums import NotificationTypeEnum
from apps.notification.utils import create_in_app_notification
from apps.teacher.models import TeacherModel


class StaffSalaryCreateView(AdminRequiredMixin, View):
    template_name = "finance/salary/create.html"

    def get(self, request):
        form = StaffSalaryCreateForm()
        return render(request, self.template_name, {"form": form})

    def post(self, request):
        form = StaffSalaryCreateForm(request.POST)

        if form.is_valid():
            salary = form.save()
            print("SALARY SAVED:", salary.pk)
            return redirect("finance:salary_list")

        print("FORM ERRORS:", form.errors)
        print("FORM NON FIELD ERRORS:", form.non_field_errors())
        print("POST DATA:", request.POST.dict())

        return render(request, self.template_name, {"form": form})


class StaffSalaryListView(AdminRequiredMixin, View):
    template_name = "finance/salary/list.html"

    def get(self, request):
        year_id = request.GET.get("year")
        search = request.GET.get("search")

        salaries = StaffSalaryModel.objects.select_related("teacher", "academic_year")

        # فیلتر سال تحصیلی
        if year_id:
            salaries = salaries.filter(academic_year_id=year_id)

        # جستجو معلم
        if search:
            salaries = salaries.filter(
                Q(teacher__user__first_name__icontains=search)
                | Q(teacher__user__last_name__icontains=search)
                | Q(teacher__national_id__icontains=search)
            )

        years = AcademicYearModel.objects.all()

        return render(
            request,
            self.template_name,
            {
                "salaries": salaries,
                "years": years,
            },
        )


class StaffSalaryUpdateView(AdminRequiredMixin, View):
    template_name = "finance/salary/update.html"

    def get(self, request, salary_id):
        salary = get_object_or_404(StaffSalaryModel, id=salary_id)
        form = StaffSalaryUpdateForm(instance=salary)
        return render(request, self.template_name, {"form": form, "salary": salary})

    def post(self, request, salary_id):
        salary = get_object_or_404(StaffSalaryModel, id=salary_id)
        form = StaffSalaryUpdateForm(request.POST, instance=salary)

        if form.is_valid():
            form.save()
            return redirect("finance:salary_list")

        return render(request, self.template_name, {"form": form, "salary": salary})


class MonthlySalaryPrepareView(AdminRequiredMixin, View):
    template_name = "finance/salary/monthly_prepare.html"

    def get(self, request):
        active_year = get_active_year(request)

        salaries = (
            StaffSalaryModel.objects.select_related(
                "teacher",
                "teacher__user",
                "academic_year",
            ).filter(academic_year=active_year)
            if active_year
            else StaffSalaryModel.objects.none()
        )

        return render(
            request,
            self.template_name,
            {
                "active_year": active_year,
                "salaries": salaries,
            },
        )


class MonthlySalaryExportView(AdminRequiredMixin, View):

    def post(self, request):
        active_year = get_active_year(request)

        if not active_year:
            return HttpResponseBadRequest(
                "سال تحصیلی فعالی برای تهیه لیست حقوق وجود ندارد."
            )

        # اعتبارسنجی ماه
        try:
            month = int(request.POST.get("month", ""))
        except (TypeError, ValueError):
            return HttpResponseBadRequest("ماه واردشده معتبر نیست.")

        if month < 1 or month > 12:
            return HttpResponseBadRequest("ماه باید بین ۱ تا ۱۲ باشد.")

        # دریافت اطلاعات ارسالی
        try:
            payload = json.loads(request.POST.get("payload") or "[]")
        except (json.JSONDecodeError, TypeError):
            return HttpResponseBadRequest("اطلاعات ارسالی معتبر نیست.")

        if not isinstance(payload, list) or not payload:
            return HttpResponseBadRequest("هیچ معلمی انتخاب نشده است.")

        # دریافت احکام معتبر سال تحصیلی فعال
        salary_queryset = StaffSalaryModel.objects.select_related(
            "teacher", "teacher__user", "academic_year"
        ).filter(academic_year=active_year)

        salary_map = {str(salary.id): salary for salary in salary_queryset}

        selected_salaries = []
        seen_ids = set()

        # اعتبارسنجی و محاسبه مبلغ حقوق در سمت سرور
        for item in payload:

            if not isinstance(item, dict):
                return HttpResponseBadRequest("ساختار اطلاعات حقوق معتبر نیست.")

            salary_id = str(item.get("salary_id", ""))

            if not salary_id or salary_id in seen_ids:
                return HttpResponseBadRequest("حکم حقوق انتخاب‌شده معتبر نیست.")

            seen_ids.add(salary_id)

            salary = salary_map.get(salary_id)

            if not salary:
                return HttpResponseBadRequest(
                    "یکی از احکام حقوق متعلق به سال تحصیلی فعال نیست."
                )

            try:
                hours = Decimal(str(item.get("hours", "")))
            except (InvalidOperation, TypeError, ValueError):
                return HttpResponseBadRequest("ساعت کارکرد یکی از معلمان معتبر نیست.")

            if not hours.is_finite() or hours < 0:
                return HttpResponseBadRequest(
                    "ساعت کارکرد نمی‌تواند منفی یا نامعتبر باشد."
                )

            hourly_rate = salary.base_amount
            amount = hourly_rate * hours

            selected_salaries.append(
                {
                    "salary": salary,
                    "teacher": salary.teacher,
                    "hourly_rate": hourly_rate,
                    "hours": hours,
                    "amount": amount,
                }
            )

        # ساخت فایل اکسل
        wb = Workbook()
        ws = wb.active
        ws.title = "لیست پرداخت حقوق"

        # استایل‌ها
        header_font = Font(bold=True, size=11)
        title_font = Font(bold=True, size=14)

        center = Alignment(
            horizontal="center",
            vertical="center",
        )

        fill = PatternFill(
            start_color="D9E1F2",
            end_color="D9E1F2",
            fill_type="solid",
        )

        thin_border = Border(
            left=Side(style="thin"),
            right=Side(style="thin"),
            top=Side(style="thin"),
            bottom=Side(style="thin"),
        )

        # عنوان
        ws.merge_cells("A1:G1")
        ws["A1"] = f"لیست پرداخت حقوق معلمان - ماه {month} " f"- سال {active_year.name}"
        ws["A1"].font = title_font
        ws["A1"].alignment = center
        ws.row_dimensions[1].height = 30

        # هدر جدول
        headers = [
            "نام معلم",
            "کد ملی",
            "سال تحصیلی",
            "ماه",
            "حقوق ساعتی",
            "ساعت کارکرد",
            "مبلغ قابل پرداخت",
        ]

        ws.append(headers)

        for cell in ws[2]:
            cell.font = header_font
            cell.alignment = center
            cell.fill = fill
            cell.border = thin_border

        # اطلاعات معلمان
        for row_number, item in enumerate(selected_salaries, start=3):

            teacher = item["teacher"]

            ws.append(
                [
                    teacher.user.full_name,
                    teacher.national_id,
                    active_year.name,
                    month,
                    float(item["hourly_rate"]),
                    float(item["hours"]),
                    float(item["amount"]),
                ]
            )

            for cell in ws[row_number]:
                cell.alignment = center
                cell.border = thin_border

            # فرمت عددی
            for column in ("E", "F", "G"):
                ws[f"{column}{row_number}"].number_format = "#,##0.##"

        # عرض ستون‌ها
        column_widths = {
            "A": 25,
            "B": 18,
            "C": 18,
            "D": 10,
            "E": 18,
            "F": 16,
            "G": 22,
        }

        for column, width in column_widths.items():
            ws.column_dimensions[column].width = width

        ws.freeze_panes = "A3"
        ws.auto_filter.ref = f"A2:G{ws.max_row}"

        # خروجی اکسل
        response = HttpResponse(
            content_type=(
                "application/vnd.openxmlformats-officedocument." "spreadsheetml.sheet"
            )
        )

        filename = f"salary_{active_year.name}_month_{month}.xlsx"

        response["Content-Disposition"] = f'attachment; filename="{filename}"'

        wb.save(response)

        return response


class SalaryPaymentCreateView(AdminRequiredMixin, View):
    template_name = "finance/salary/payment_create.html"

    def get(self, request, salary_id):
        salary = get_object_or_404(StaffSalaryModel, id=salary_id)
        form = SalaryPaymentCreateForm(salary=salary)
        return render(request, self.template_name, {"form": form, "salary": salary})

    def post(self, request, salary_id):
        salary = get_object_or_404(
            StaffSalaryModel.objects.select_related("teacher", "teacher__user"),
            id=salary_id,
        )

        form = SalaryPaymentCreateForm(request.POST, salary=salary)

        if form.is_valid():
            payment = form.save(commit=False)
            payment.salary = salary
            payment.save()

            create_in_app_notification(
                to_user=salary.teacher.user,
                notification_type=NotificationTypeEnum.TUITION_PAYMENT,
                title="پرداخت حقوق",
                description=(
                    f"مبلغ {payment.amount:,} بابت حقوق شما "
                    f"در تاریخ {payment.payment_date.date()} ثبت و پرداخت شد."
                ),
            )

            messages.success(request, "پرداخت حقوق با موفقیت ثبت شد.")
            return redirect("finance:salary_list")

        return render(
            request,
            self.template_name,
            {"form": form, "salary": salary},
        )


class StaffSalaryDetailView(AdminRequiredMixin, View):
    template_name = "finance/salary/detail.html"

    def get(self, request, salary_id):
        salary = get_object_or_404(StaffSalaryModel, id=salary_id)

        # سال فعال
        active_year = get_active_year(request)

        # سال انتخاب‌شده توسط کاربر
        year_id = request.GET.get("year")

        years = AcademicYearModel.objects.all()

        # پرداخت‌ها
        payments = salary.payments.all()

        # اگر کاربر سال انتخاب کرده باشد → همان را اعمال کن
        if year_id:
            payments = payments.filter(salary__academic_year_id=year_id)
            selected_year = AcademicYearModel.objects.get(id=year_id)

        # اگر کاربر سال انتخاب نکرده باشد → سال فعال را اعمال کن
        else:
            payments = payments.filter(salary__academic_year=active_year)
            selected_year = active_year

        # مجموع پرداخت‌ها
        total_paid = payments.aggregate(total=Sum("amount"))["total"] or 0

        return render(
            request,
            self.template_name,
            {
                "salary": salary,
                "payments": payments,
                "years": years,
                "selected_year": selected_year,
                "total_paid": total_paid,
            },
        )


class TeacherSalaryDashboardView(AdminRequiredMixin, View):
    template_name = "teacher/salary.html"

    def get(self, request):
        # معلم لاگین‌شده
        teacher = get_object_or_404(TeacherModel, user=request.user)

        # سال فعال
        active_year = get_active_year(request)

        # سال انتخاب‌شده توسط کاربر
        year_id = request.GET.get("year")

        years = AcademicYearModel.objects.all()

        # حکم‌های معلم
        salaries = StaffSalaryModel.objects.filter(teacher=teacher)

        # انتخاب سال
        if year_id:
            selected_year = AcademicYearModel.objects.get(id=year_id)
        else:
            selected_year = active_year

        # حکم سال انتخاب‌شده
        salary = salaries.filter(academic_year=selected_year).first()

        payments = []
        total_paid = 0
        remaining = 0

        if salary:
            payments = salary.payments.all()
            total_paid = payments.aggregate(total=Sum("amount"))["total"] or 0
            remaining = salary.base_amount - total_paid

        return render(
            request,
            self.template_name,
            {
                "teacher": teacher,
                "salary": salary,
                "payments": payments,
                "years": years,
                "selected_year": selected_year,
                "total_paid": total_paid,
            },
        )
