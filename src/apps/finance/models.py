from django.db import models

from apps.core.models import BaseModel
from apps.finance import enums


class TuitionModel(BaseModel):
    Status = enums.TuitionStatusEnum

    student = models.ForeignKey(
        "student.StudentModel",
        on_delete=models.PROTECT,
        related_name="tuitions",
        verbose_name="دانش‌آموز",
    )

    academic_year = models.ForeignKey(
        "academic.AcademicYearModel",
        on_delete=models.PROTECT,
        related_name="tuitions",
        verbose_name="سال تحصیلی",
    )

    amount = models.DecimalField(
        max_digits=14, decimal_places=0, verbose_name="مبلغ شهریه"
    )
    discount = models.DecimalField(
        max_digits=14, decimal_places=0, default=0, verbose_name="تخفیف"
    )

    status = models.CharField(
        max_length=20,
        choices=Status.choices,
        default=Status.PENDING,
        verbose_name="وضعیت",
    )

    description = models.TextField(blank=True, verbose_name="توضیحات")

    class Meta:
        verbose_name = "شهریه"
        verbose_name_plural = "شهریه ها"

    @property
    def final_amount(self):
        return self.amount - self.discount

    @property
    def paid_amount(self):
        return sum(p.amount for p in self.payments.all())

    @property
    def remaining_amount(self):
        return self.final_amount - self.paid_amount

    def update_status(self):
        if self.remaining_amount <= 0:
            self.status = self.Status.PAID
        else:
            self.status = self.Status.PENDING
        self.save()

    def __str__(self):
        return f"{self.student} - {self.academic_year}"


class PaymentRecordModel(BaseModel):
    Status = enums.PaymentStatusEnum
    Method = enums.PaymentMethodEnum

    student = models.ForeignKey(
        "student.StudentModel",
        on_delete=models.PROTECT,
        related_name="payment_records",
        verbose_name="دانش‌آموز",
    )

    tuition = models.ForeignKey(
        "finance.TuitionModel",
        on_delete=models.PROTECT,
        related_name="payments",
        null=True,
        blank=True,
        verbose_name="شهریه",
    )

    amount = models.DecimalField(
        max_digits=14,
        decimal_places=0,
        verbose_name="مبلغ پرداخت",
    )

    payment_method = models.CharField(
        max_length=20,
        choices=Method.choices,
        verbose_name="روش پرداخت",
    )

    description = models.TextField(
        blank=True,
        verbose_name="توضیحات",
    )

    class Meta:
        verbose_name = "پرداخت شهریه"
        verbose_name_plural = "پرداخت های شهریه"

    def __str__(self):
        return f"{self.student} - {self.tuition}"


class StaffSalaryModel(BaseModel):

    teacher = models.ForeignKey(
        "teacher.TeacherModel",
        on_delete=models.PROTECT,
        related_name="salaries",
        verbose_name="معلم",
    )

    academic_year = models.ForeignKey(
        "academic.AcademicYearModel",
        on_delete=models.PROTECT,
        related_name="staff_salaries",
        verbose_name="سال تحصیلی",
    )

    base_amount = models.DecimalField(
        max_digits=14,
        decimal_places=0,
        verbose_name="حقوق پایه",
    )

    description = models.TextField(
        blank=True,
        verbose_name="توضیحات",
    )

    class Meta:
        verbose_name = "حقوق معلم"
        verbose_name_plural = "حقوق معلمان"

    def __str__(self):
        return f"{self.teacher} - {self.base_amount}"


class SalaryPaymentModel(BaseModel):
    Method = enums.PaymentMethodEnum

    salary = models.ForeignKey(
        "finance.StaffSalaryModel",
        on_delete=models.PROTECT,
        related_name="payments",
        verbose_name="حقوق",
    )

    amount = models.DecimalField(
        max_digits=14,
        decimal_places=0,
        verbose_name="مبلغ پرداخت",
    )

    payment_date = models.DateTimeField(verbose_name="تاریخ پرداخت", auto_now=True)

    description = models.TextField(
        blank=True,
        verbose_name="توضیحات",
    )

    class Meta:
        verbose_name = "پرداخت حقوق"
        verbose_name_plural = "پرداخت‌های حقوق"
        ordering = ("-payment_date",)

    def __str__(self):
        return f"{self.salary} - {self.payment_date}"


class SchoolExpenseModel(BaseModel):
    Category = enums.ExpenseCategoryEnum

    academic_year = models.ForeignKey(
        "academic.AcademicYearModel",
        on_delete=models.CASCADE,  # ← مشکل حل شد
        related_name="expenses",
        verbose_name="سال تحصیلی",
    )

    title = models.CharField(max_length=200)
    category = models.CharField(max_length=30, choices=Category.choices)
    amount = models.DecimalField(max_digits=14, decimal_places=0)
    description = models.TextField(blank=True)

    class Meta:
        verbose_name = "هزینه مدرسه"
        verbose_name_plural = "هزینه‌های مدرسه"
