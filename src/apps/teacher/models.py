from django.db import models

from apps.core.models import BaseModel
from apps.teacher.enums import EmploymentTypeEnum, TeacherStatusEnum


class TeacherModel(BaseModel):
    Status = TeacherStatusEnum
    EmploymentType = EmploymentTypeEnum

    user = models.OneToOneField(
        "account.User",
        on_delete=models.CASCADE,
        related_name="teacher",
        verbose_name="حساب کاربری",
    )

    national_id = models.CharField(
        max_length=10,
        unique=True,
        verbose_name="کد ملی",
    )

    status = models.CharField(
        max_length=20,
        choices=Status.choices,
        default=Status.ACTIVE,
        verbose_name="وضعیت همکاری",
    )

    employment_type = models.CharField(
        max_length=20,
        choices=EmploymentType.choices,
        default=EmploymentType.FULL_TIME,
        verbose_name="نوع همکاری",
    )

    education = models.CharField(
        max_length=128,
        blank=True,
        verbose_name="مدرک تحصیلی",
    )

    specialization = models.CharField(
        max_length=128,
        blank=True,
        verbose_name="تخصص",
    )

    class Meta:
        verbose_name = "معلم"
        verbose_name_plural = "معلمان"
        ordering = ("-created_at",)

    def __str__(self):
        return f"{self.national_id} - {self.user.full_name}"


class TeacherNoteModel(BaseModel):
    teacher = models.ForeignKey(
        "teacher.TeacherModel",
        on_delete=models.CASCADE,
        related_name="notes",
        verbose_name="معلم",
    )

    attendance_session = models.ForeignKey(
        "attendance.AttendanceSessionModel",
        on_delete=models.CASCADE,
        related_name="teacher_notes",
        null=True,
        blank=True,
        verbose_name="جلسه",
    )

    title = models.CharField(
        max_length=200,
        verbose_name="عنوان",
    )

    content = models.TextField(
        verbose_name="متن یادداشت",
    )

    is_completed = models.BooleanField(
        default=False,
        verbose_name="انجام شده",
    )

    class Meta:
        verbose_name = "یادداشت معلم"
        verbose_name_plural = "یادداشت‌های معلمان"
        ordering = ("-created_at",)

    def __str__(self):
        return f"{self.teacher} - {self.title}"


class EmploymentRecordModel(BaseModel):
    teacher = models.ForeignKey(
        "teacher.TeacherModel",
        on_delete=models.CASCADE,
        related_name="employment_records",
        verbose_name="معلم",
    )

    employment_type = models.CharField(
        max_length=20,
        choices=EmploymentTypeEnum.choices,
        verbose_name="نوع همکاری",
    )

    start_date = models.DateField(
        verbose_name="تاریخ شروع",
    )

    end_date = models.DateField(
        null=True,
        blank=True,
        verbose_name="تاریخ پایان",
    )

    description = models.TextField(
        blank=True,
        verbose_name="توضیحات",
    )

    class Meta:
        verbose_name = "سابقه همکاری"
        verbose_name_plural = "سوابق همکاری"
        ordering = ("-start_date",)

    def __str__(self):
        return f"{self.teacher} - {self.start_date}"
