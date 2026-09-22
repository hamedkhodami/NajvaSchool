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
        max_digits=14,
        decimal_places=0,
        verbose_name="مبلغ شهریه",
    )

    discount = models.DecimalField(
        max_digits=14,
        decimal_places=0,
        default=0,
        verbose_name="تخفیف",
    )

    status = models.CharField(
        max_length=20,
        choices=Status.choices,
        default=Status.PENDING,
        verbose_name="وضعیت",
    )

    description = models.TextField(
        blank=True,
        verbose_name="توضیحات",
    )

    class Meta:
        verbose_name = "شهریه"
        verbose_name_plural = "شهریه ها"

    def __str__(self):
        return f"{self.student} - {self.academic_year}"


class TuitionInstallmentModel(BaseModel):
    tuition = models.ForeignKey(
        "finance.TuitionModel",
        on_delete=models.CASCADE,
        related_name="installments",
        verbose_name="شهریه",
    )

    installment_number = models.PositiveSmallIntegerField(
        verbose_name="شماره قسط",
    )

    amount = models.DecimalField(
        max_digits=14,
        decimal_places=0,
        verbose_name="مبلغ قسط",
    )

    due_date = models.DateField(
        null=True,
        blank=True,
        verbose_name="سررسید",
    )

    description = models.TextField(
        blank=True,
        verbose_name="توضیحات",
    )

    class Meta:
        verbose_name = "قسط شهریه"
        verbose_name_plural = "اقساط شهریه"
        ordering = ("installment_number",)

        constraints = [
            models.UniqueConstraint(
                fields=("tuition", "installment_number"),
                name="unique_tuition_installment",
            )
        ]

    def __str__(self):
        return f"{self.tuition} - {self.installment_number}"


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

    installment = models.ForeignKey(
        "finance.TuitionInstallmentModel",
        on_delete=models.PROTECT,
        related_name="payments",
        null=True,
        blank=True,
        verbose_name="قسط",
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

    status = models.CharField(
        max_length=20,
        choices=Status.choices,
        default=Status.PAID,
        verbose_name="وضعیت پرداخت",
    )

    payment_date = models.DateTimeField(
        verbose_name="تاریخ پرداخت",
    )

    tracking_code = models.CharField(
        max_length=100,
        blank=True,
        verbose_name="کد پیگیری",
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
    Status = enums.SalaryStatusEnum

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

    year = models.PositiveSmallIntegerField(
        verbose_name="سال",
    )

    month = models.PositiveSmallIntegerField(
        verbose_name="ماه",
    )

    base_amount = models.DecimalField(
        max_digits=14,
        decimal_places=0,
        verbose_name="حقوق پایه",
    )

    bonus_amount = models.DecimalField(
        max_digits=14,
        decimal_places=0,
        default=0,
        verbose_name="پاداش و اضافه پرداخت",
    )

    deduction_amount = models.DecimalField(
        max_digits=14,
        decimal_places=0,
        default=0,
        verbose_name="کسورات",
    )

    final_amount = models.DecimalField(
        max_digits=14,
        decimal_places=0,
        verbose_name="حقوق نهایی",
    )

    status = models.CharField(
        max_length=20,
        choices=Status.choices,
        default=Status.PENDING,
        verbose_name="وضعیت",
    )

    description = models.TextField(
        blank=True,
        verbose_name="توضیحات",
    )

    class Meta:
        verbose_name = "حقوق معلم"
        verbose_name_plural = "حقوق معلمان"
        ordering = ("-year", "-month")

        constraints = [
            models.UniqueConstraint(
                fields=("teacher", "year", "month"),
                name="unique_teacher_salary_per_month",
            )
        ]

    def __str__(self):
        return f"{self.teacher} - {self.year} - {self.month}"


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

    payment_date = models.DateTimeField(
        verbose_name="تاریخ پرداخت",
    )

    payment_method = models.CharField(
        max_length=20,
        choices=Method.choices,
        verbose_name="روش پرداخت",
    )

    tracking_code = models.CharField(
        max_length=100,
        blank=True,
        verbose_name="کد پیگیری",
    )

    description = models.TextField(
        blank=True,
        verbose_name="توضیحات",
    )

    class Meta:
        verbose_name = "پرداخت حقوق"
        verbose_name_plural = "پرداخت‌های حقوق"
        ordering = ("-payment_date",)

    def __str__(self):
        return f"{self.salary} - {self.payment_method}"


class SchoolExpenseModel(BaseModel):
    Category = enums.ExpenseCategoryEnum

    title = models.CharField(
        max_length=200,
        verbose_name="عنوان هزینه",
    )

    category = models.CharField(
        max_length=30,
        choices=Category.choices,
        verbose_name="دسته‌بندی",
    )

    amount = models.DecimalField(
        max_digits=14,
        decimal_places=0,
        verbose_name="مبلغ",
    )

    expense_date = models.DateField(
        verbose_name="تاریخ هزینه",
    )

    description = models.TextField(
        blank=True,
        verbose_name="توضیحات",
    )

    receipt_number = models.CharField(
        max_length=100,
        blank=True,
        verbose_name="شماره رسید",
    )

    class Meta:
        verbose_name = "هزینه مدرسه"
        verbose_name_plural = "هزینه‌های مدرسه"
        ordering = ("-expense_date",)

    def __str__(self):
        return f"{self.category} - {self.title}"
