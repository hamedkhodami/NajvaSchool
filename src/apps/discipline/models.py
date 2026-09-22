from django.db import models

from apps.core.models import BaseModel
from apps.discipline import enums


class DisciplineTypeModel(BaseModel):
    Effect = enums.DisciplineEffectEnum

    name = models.CharField(
        max_length=100,
        unique=True,
        verbose_name="عنوان",
    )

    effect = models.CharField(
        max_length=20,
        choices=Effect.choices,
        verbose_name="نوع اثر",
    )

    description = models.TextField(
        blank=True,
        verbose_name="توضیحات",
    )

    is_active = models.BooleanField(
        default=True,
        verbose_name="فعال",
    )

    class Meta:
        verbose_name = "نوع انضباطی"
        verbose_name_plural = "انواع انضباطی"
        ordering = ("name",)

    def __str__(self):
        return self.name


class DisciplineRecordModel(BaseModel):
    student = models.ForeignKey(
        "student.StudentModel",
        on_delete=models.PROTECT,
        related_name="discipline_records",
        verbose_name="دانش‌آموز",
    )

    discipline_type = models.ForeignKey(
        "discipline.DisciplineTypeModel",
        on_delete=models.PROTECT,
        related_name="records",
        verbose_name="نوع انضباطی",
    )

    recorder = models.ForeignKey(
        "account.User",
        on_delete=models.PROTECT,
        related_name="discipline_records",
        verbose_name="ثبت‌کننده",
    )

    classroom = models.ForeignKey(
        "academic.ClassroomModel",
        on_delete=models.PROTECT,
        related_name="discipline_records",
        null=True,
        blank=True,
        verbose_name="کلاس",
    )

    date = models.DateField(
        verbose_name="تاریخ",
    )

    title = models.CharField(
        max_length=200,
        verbose_name="عنوان",
    )

    description = models.TextField(
        blank=True,
        verbose_name="توضیحات",
    )

    class Meta:
        verbose_name = "سابقه انضباطی"
        verbose_name_plural = "سوابق انضباطی"
        ordering = ("-date", "-created_at")

    def __str__(self):
        return f"{self.student} - {self.title}"


class BehavioralEvaluationModel(BaseModel):
    student = models.ForeignKey(
        "student.StudentModel",
        on_delete=models.PROTECT,
        related_name="behavioral_evaluations",
        verbose_name="دانش‌آموز",
    )

    evaluator = models.ForeignKey(
        "account.User",
        on_delete=models.PROTECT,
        related_name="behavioral_evaluations",
        verbose_name="ارزیابی‌کننده",
    )

    classroom = models.ForeignKey(
        "academic.ClassroomModel",
        on_delete=models.PROTECT,
        related_name="behavioral_evaluations",
        null=True,
        blank=True,
        verbose_name="کلاس",
    )

    evaluation_date = models.DateField(
        verbose_name="تاریخ ارزیابی",
    )

    title = models.CharField(
        max_length=200,
        verbose_name="عنوان ارزیابی",
    )

    level = models.CharField(
        max_length=20,
        choices=enums.BehavioralEvaluationLevelEnum.choices,
        verbose_name="سطح ارزیابی",
    )

    description = models.TextField(
        blank=True,
        verbose_name="توضیحات",
    )

    class Meta:
        verbose_name = "ارزیابی رفتاری"
        verbose_name_plural = "ارزیابی‌های رفتاری"
        ordering = ("-evaluation_date", "-created_at")

    def __str__(self):
        return f"{self.student} - {self.title}"


class EducationalRecordModel(BaseModel):
    student = models.ForeignKey(
        "student.StudentModel",
        on_delete=models.PROTECT,
        related_name="educational_records",
        verbose_name="دانش‌آموز",
    )

    recorder = models.ForeignKey(
        "account.User",
        on_delete=models.PROTECT,
        related_name="educational_records",
        verbose_name="ثبت‌کننده",
    )

    classroom = models.ForeignKey(
        "academic.ClassroomModel",
        on_delete=models.PROTECT,
        related_name="educational_records",
        null=True,
        blank=True,
        verbose_name="کلاس",
    )

    record_type = models.CharField(
        max_length=30,
        choices=enums.EducationalRecordTypeEnum.choices,
        verbose_name="نوع سابقه",
    )

    title = models.CharField(
        max_length=200,
        verbose_name="عنوان",
    )

    date = models.DateField(
        verbose_name="تاریخ",
    )

    description = models.TextField(
        blank=True,
        verbose_name="توضیحات",
    )

    class Meta:
        verbose_name = "سابقه تربیتی"
        verbose_name_plural = "سوابق تربیتی"
        ordering = ("-date", "-created_at")

    def __str__(self):
        return f"{self.student} - {self.title}"
