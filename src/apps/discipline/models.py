from django.db import models

from apps.core.models import BaseModel
from apps.discipline import enums


class StudentDevelopmentRecordModel(BaseModel):
    RecordCategory = enums.StudentRecordCategoryEnum
    DisciplineEffect = enums.DisciplineEffectEnum
    BehavioralLevel = enums.BehavioralEvaluationLevelEnum
    EducationalType = enums.EducationalRecordTypeEnum

    student = models.ForeignKey(
        "student.StudentModel",
        on_delete=models.PROTECT,
        related_name="development_records",
        verbose_name="دانش‌آموز",
    )

    recorder = models.ForeignKey(
        "account.User",
        on_delete=models.PROTECT,
        related_name="development_records",
        verbose_name="ثبت‌کننده",
    )

    classroom = models.ForeignKey(
        "academic.ClassroomModel",
        on_delete=models.PROTECT,
        related_name="development_records",
        null=True,
        blank=True,
        verbose_name="کلاس",
    )

    category = models.CharField(
        max_length=30,
        choices=RecordCategory.choices,
        verbose_name="دسته",
    )

    effect = models.CharField(
        max_length=20,
        choices=DisciplineEffect.choices,
        null=True,
        blank=True,
        verbose_name="اثر انضباطی",
    )

    level = models.CharField(
        max_length=20,
        choices=BehavioralLevel.choices,
        null=True,
        blank=True,
        verbose_name="سطح رفتاری",
    )

    educational_type = models.CharField(
        max_length=30,
        choices=EducationalType.choices,
        null=True,
        blank=True,
        verbose_name="نوع تربیتی",
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
        verbose_name = "سابقه پرورشی"
        verbose_name_plural = "سوابق پرورشی"
        ordering = ("-date", "-created_at")

    def __str__(self):
        return f"{self.student} - {self.title}"
