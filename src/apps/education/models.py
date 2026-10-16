from django.db import models

from apps.core.models import BaseModel


class ExamModel(BaseModel):
    classroom = models.ForeignKey(
        "academic.ClassroomModel",
        on_delete=models.PROTECT,
        related_name="exams",
        verbose_name="کلاس",
    )

    subject = models.ForeignKey(
        "academic.SubjectModel",
        on_delete=models.PROTECT,
        related_name="exams",
        verbose_name="درس",
    )

    teacher = models.ForeignKey(
        "teacher.TeacherModel",
        on_delete=models.PROTECT,
        related_name="exams",
        verbose_name="معلم",
    )
    description = models.TextField(
        blank=True,
        verbose_name="توضیحات",
    )

    max_score = models.DecimalField(
        max_digits=5,
        decimal_places=2,
        default=20,
        verbose_name="نمره کل",
    )

    duration = models.PositiveIntegerField(
        null=True,
        blank=True,
        verbose_name="مدت امتحان (دقیقه)",
    )

    file = models.FileField(
        upload_to="education/exams/", blank=True, null=True, verbose_name="فایل"
    )

    is_published = models.BooleanField(
        default=False,
        verbose_name="اعلام نتایج",
    )

    class Meta:
        verbose_name = "امتحان"
        verbose_name_plural = "امتحانات"
        ordering = ("-created_at",)

    def __str__(self):
        return f"{self.title} - {self.classroom}"


class ExamResultModel(BaseModel):
    exam = models.ForeignKey(
        "education.ExamModel",
        on_delete=models.CASCADE,
        related_name="results",
        verbose_name="امتحان",
    )

    student = models.ForeignKey(
        "student.StudentModel",
        on_delete=models.PROTECT,
        related_name="exam_results",
        verbose_name="دانش‌آموز",
    )

    score = models.DecimalField(
        max_digits=5,
        decimal_places=2,
        verbose_name="نمره",
    )

    description = models.TextField(
        null=True,
        blank=True,
        verbose_name="توضیحات",
    )

    class Meta:
        verbose_name = "نتیجه امتحان"
        verbose_name_plural = "نتایج امتحانات"
        ordering = ("-created_at",)
        constraints = [
            models.UniqueConstraint(
                fields=("exam", "student"),
                name="unique_exam_result_per_student",
            )
        ]

    def __str__(self):
        return f"{self.student} - {self.exam} - {self.score}"


class DailyGradeModel(BaseModel):
    student = models.ForeignKey(
        "student.StudentModel",
        on_delete=models.PROTECT,
        related_name="daily_grades",
        verbose_name="دانش‌آموز",
    )

    teacher = models.ForeignKey(
        "teacher.TeacherModel",
        on_delete=models.PROTECT,
        related_name="daily_grades",
        verbose_name="معلم",
    )

    classroom = models.ForeignKey(
        "academic.ClassroomModel",
        on_delete=models.PROTECT,
        related_name="daily_grades",
        verbose_name="کلاس",
    )

    subject = models.ForeignKey(
        "academic.SubjectModel",
        on_delete=models.PROTECT,
        related_name="daily_grades",
        verbose_name="درس",
    )

    title = models.CharField(
        max_length=200,
        verbose_name="عنوان",
    )

    score = models.DecimalField(
        max_digits=5,
        decimal_places=2,
        verbose_name="نمره",
    )

    description = models.TextField(
        blank=True,
        verbose_name="توضیحات",
    )

    class Meta:
        verbose_name = "نمره روزانه"
        verbose_name_plural = "نمرات روزانه"
        ordering = ("-created_at",)

    def __str__(self):
        return f"{self.student} - {self.subject} - {self.score}"
