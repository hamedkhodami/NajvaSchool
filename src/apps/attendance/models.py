from django.db import models

from apps.attendance.enums import AttendanceStatusEnum, StaffAttendanceStatusEnum
from apps.core.models import BaseModel


class AttendanceSessionModel(BaseModel):
    classroom = models.ForeignKey(
        "academic.ClassroomModel",
        on_delete=models.PROTECT,
        related_name="attendance_sessions",
        verbose_name="کلاس",
    )

    schedule_session = models.ForeignKey(
        "academic.ScheduleSessionModel",
        on_delete=models.PROTECT,
        related_name="attendance_sessions",
        null=True,
        blank=True,
        verbose_name="جلسه برنامه هفتگی",
    )

    date = models.DateField(
        verbose_name="تاریخ",
    )

    session_number = models.PositiveSmallIntegerField(
        verbose_name="شماره جلسه",
    )

    description = models.TextField(
        blank=True,
        verbose_name="توضیحات",
    )

    class Meta:
        verbose_name = "جلسه حضور و غیاب"
        verbose_name_plural = "جلسات حضور و غیاب"
        ordering = ("-date", "session_number")

    def __str__(self):
        return f"{self.classroom} - {self.date} - جلسه {self.session_number}"


class StudentAttendanceModel(BaseModel):
    Status = AttendanceStatusEnum

    session = models.ForeignKey(
        "attendance.AttendanceSessionModel",
        on_delete=models.CASCADE,
        related_name="student_attendances",
        verbose_name="جلسه حضور و غیاب",
    )

    student = models.ForeignKey(
        "student.StudentModel",
        on_delete=models.PROTECT,
        related_name="attendances",
        verbose_name="دانش‌آموز",
    )

    status = models.CharField(
        max_length=20,
        choices=Status.choices,
        default=Status.PRESENT,
        verbose_name="وضعیت حضور",
    )

    arrival_time = models.TimeField(
        null=True,
        blank=True,
        verbose_name="زمان ورود",
    )

    description = models.TextField(
        blank=True,
        verbose_name="توضیحات",
    )

    class Meta:
        verbose_name = "حضور و غیاب دانش‌آموز"
        verbose_name_plural = "حضور و غیاب دانش‌آموزان"
        ordering = ("-created_at",)
        constraints = [
            models.UniqueConstraint(
                fields=("session", "student"),
                name="unique_student_attendance_per_session",
            )
        ]

    def __str__(self):
        return f"{self.student} - {self.session} - {self.status}"


class StaffAttendanceModel(BaseModel):
    Status = StaffAttendanceStatusEnum

    teacher = models.ForeignKey(
        "teacher.TeacherModel",
        on_delete=models.PROTECT,
        related_name="attendances",
        verbose_name="معلم",
    )

    date = models.DateField(
        verbose_name="تاریخ",
    )

    status = models.CharField(
        max_length=20,
        choices=Status.choices,
        default=Status.PRESENT,
        verbose_name="وضعیت حضور",
    )

    arrival_time = models.TimeField(
        null=True,
        blank=True,
        verbose_name="زمان ورود",
    )

    departure_time = models.TimeField(
        null=True,
        blank=True,
        verbose_name="زمان خروج",
    )

    description = models.TextField(
        blank=True,
        verbose_name="توضیحات",
    )

    class Meta:
        verbose_name = "حضور و غیاب معلم"
        verbose_name_plural = "حضور و غیاب معلمان"
        ordering = ("-date",)

        constraints = [
            models.UniqueConstraint(
                fields=("teacher", "date"),
                name="unique_teacher_attendance_per_day",
            )
        ]

    def __str__(self):
        return f"{self.teacher} - {self.date} - {self.status}"
