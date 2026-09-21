from django.db import models

from apps.academic import enums
from apps.core.models import BaseModel


class AcademicYearModel(BaseModel):
    Status = enums.AcademicYearStatusEnum

    name = models.CharField(
        max_length=20,
        unique=True,
        verbose_name="عنوان سال تحصیلی",
    )

    start_date = models.DateField(
        verbose_name="تاریخ شروع",
    )

    end_date = models.DateField(
        verbose_name="تاریخ پایان",
    )

    status = models.CharField(
        max_length=20,
        choices=Status.choices,
        default=Status.PLANNED,
        verbose_name="وضعیت",
    )

    class Meta:
        verbose_name = "سال تحصیلی"
        verbose_name_plural = "سال‌های تحصیلی"
        ordering = ("-start_date",)

    def __str__(self):
        return self.name


class GradeModel(BaseModel):
    name = models.CharField(
        max_length=100,
        verbose_name="نام پایه",
    )

    code = models.CharField(
        max_length=20,
        unique=True,
        verbose_name="کد پایه",
    )

    description = models.TextField(
        blank=True,
        verbose_name="توضیحات",
    )

    class Meta:
        verbose_name = "پایه تحصیلی"
        verbose_name_plural = "پایه‌های تحصیلی"
        ordering = ("name",)

    def __str__(self):
        return self.name


class ClassroomModel(BaseModel):
    Status = enums.ClassroomStatusEnum

    academic_year = models.ForeignKey(
        "academic.AcademicYearModel",
        on_delete=models.PROTECT,
        related_name="classrooms",
        verbose_name="سال تحصیلی",
    )

    grade = models.ForeignKey(
        "academic.GradeModel",
        on_delete=models.PROTECT,
        related_name="classrooms",
        verbose_name="پایه",
    )

    name = models.CharField(
        max_length=100,
        verbose_name="نام کلاس",
    )

    code = models.CharField(
        max_length=30,
        verbose_name="کد کلاس",
    )

    capacity = models.PositiveIntegerField(
        default=30,
        verbose_name="ظرفیت کلاس",
    )

    status = models.CharField(
        max_length=20,
        choices=Status.choices,
        default=Status.ACTIVE,
        verbose_name="وضعیت",
    )

    class Meta:
        verbose_name = "کلاس"
        verbose_name_plural = "کلاس‌ها"
        ordering = ("-created_at",)

    def __str__(self):
        return f"{self.name} - {self.grade.name}"


class SubjectModel(BaseModel):
    name = models.CharField(
        max_length=100,
        verbose_name="نام درس",
    )

    code = models.CharField(
        max_length=30,
        unique=True,
        verbose_name="کد درس",
    )

    description = models.TextField(
        blank=True,
        verbose_name="توضیحات",
    )

    class Meta:
        verbose_name = "درس"
        verbose_name_plural = "دروس"
        ordering = ("name",)

    def __str__(self):
        return self.name


class StudentEnrollmentModel(BaseModel):
    Status = enums.EnrollmentStatusEnum

    student = models.ForeignKey(
        "student.StudentModel",
        on_delete=models.PROTECT,
        related_name="enrollments",
        verbose_name="دانش‌آموز",
    )

    classroom = models.ForeignKey(
        "academic.ClassroomModel",
        on_delete=models.PROTECT,
        related_name="student_enrollments",
        verbose_name="کلاس",
    )

    status = models.CharField(
        max_length=20,
        choices=Status.choices,
        default=Status.ACTIVE,
        verbose_name="وضعیت ثبت‌نام",
    )

    enrollment_date = models.DateField(
        null=True,
        blank=True,
        verbose_name="تاریخ ثبت‌نام",
    )

    class Meta:
        verbose_name = "ثبت‌نام دانش‌آموز"
        verbose_name_plural = "ثبت‌نام‌های دانش‌آموزان"
        ordering = ("-created_at",)

    def __str__(self):
        return f"{self.student} - {self.classroom}"


class ScheduleSessionModel(BaseModel):
    Week = enums.WeekDayEnum

    classroom = models.ForeignKey(
        "academic.ClassroomModel",
        on_delete=models.CASCADE,
        related_name="schedule_sessions",
        verbose_name="کلاس",
    )

    subject = models.ForeignKey(
        "academic.SubjectModel",
        on_delete=models.PROTECT,
        related_name="schedule_sessions",
        verbose_name="درس",
    )

    teacher = models.ForeignKey(
        "teacher.TeacherModel",
        on_delete=models.PROTECT,
        related_name="schedule_sessions",
        verbose_name="معلم",
    )

    weekday = models.CharField(
        max_length=20,
        choices=Week.choices,
        verbose_name="روز هفته",
    )

    start_time = models.TimeField(
        verbose_name="زمان شروع",
    )

    end_time = models.TimeField(
        verbose_name="زمان پایان",
    )

    session_number = models.PositiveSmallIntegerField(
        verbose_name="شماره جلسه",
    )

    class Meta:
        verbose_name = "جلسه برنامه هفتگی"
        verbose_name_plural = "جلسات برنامه هفتگی"
        ordering = ("weekday", "session_number")

    def __str__(self):
        return f"{self.classroom} - {self.subject} - {self.teacher}"
