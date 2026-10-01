from django.db import models

from apps.core.models import BaseModel
from apps.student.enums import StudentStatusEnum


class StudentModel(BaseModel):
    Status = StudentStatusEnum

    user = models.OneToOneField(
        "account.User",
        on_delete=models.CASCADE,
        related_name="student",
        verbose_name="حساب کاربری",
    )

    national_id = models.CharField(
        max_length=10,
        unique=True,
        verbose_name="کد ملی",
    )
    father_name = models.CharField(
        max_length=128, null=True, blank=True, verbose_name="نام پدر"
    )

    parent_phone_number = models.CharField(
        max_length=11, null=True, blank=True, verbose_name="شماره تماس اولیاء"
    )

    birth_date = models.CharField(
        max_length=12,
        null=True,
        blank=True,
        verbose_name="تاریخ تولد",
    )

    address = models.TextField(
        blank=True,
        verbose_name="آدرس",
    )

    status = models.CharField(
        max_length=20,
        choices=Status.choices,
        default=Status.ACTIVE,
        verbose_name="وضعیت دانش‌آموز",
    )

    class Meta:
        verbose_name = "دانش‌آموز"
        verbose_name_plural = "دانش‌آموزان"
        ordering = ("-created_at",)

    def __str__(self):
        return f"{self.national_id} - {self.user.full_name}"
