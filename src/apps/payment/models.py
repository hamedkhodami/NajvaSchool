from django.db import models

from apps.core.models import BaseModel
from apps.finance.enums import PaymentMethodEnum, PaymentStatusEnum


class PaymentModel(BaseModel):
    Status = PaymentStatusEnum
    Method = PaymentMethodEnum

    student = models.ForeignKey(
        "student.StudentModel",
        on_delete=models.PROTECT,
        related_name="payments",
        verbose_name="دانش‌آموز",
    )

    tuition = models.ForeignKey(
        "finance.TuitionModel",
        on_delete=models.PROTECT,
        related_name="payment_transactions",
        verbose_name="شهریه",
    )

    installment = models.ForeignKey(
        "finance.TuitionInstallmentModel",
        on_delete=models.PROTECT,
        related_name="payment_transactions",
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
        default=Status.PENDING,
        verbose_name="وضعیت پرداخت",
    )

    authority = models.CharField(
        max_length=255,
        blank=True,
        verbose_name="شناسه درگاه",
    )

    tracking_code = models.CharField(
        max_length=100,
        blank=True,
        verbose_name="کد پیگیری",
    )

    paid_at = models.DateTimeField(
        null=True,
        blank=True,
        verbose_name="زمان پرداخت",
    )

    expire_at = models.DateTimeField(
        null=True,
        blank=True,
        verbose_name="زمان انقضا",
    )

    description = models.TextField(
        blank=True,
        verbose_name="توضیحات",
    )

    ref_id = models.CharField(
        max_length=255, blank=True, null=True, verbose_name="آیدی"
    )

    card_pan = models.CharField(
        max_length=30, blank=True, null=True, verbose_name="کارت"
    )

    class Meta:
        verbose_name = "پرداخت"
        verbose_name_plural = "پرداخت‌ها"
        ordering = ("-created_at",)

    def __str__(self):
        return f"{self.student} - {self.amount} - {self.status}"
