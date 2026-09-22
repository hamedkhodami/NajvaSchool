from django.db.models import TextChoices


class AttendanceStatusEnum(TextChoices):
    PRESENT = "present", "حاضر"
    ABSENT = "absent", "غایب"
    LATE = "late", "تاخیر"
    EXCUSED = "excused", "غیبت موجه"


class StaffAttendanceStatusEnum(TextChoices):
    PRESENT = "present", "حاضر"
    ABSENT = "absent", "غایب"
    LATE = "late", "تاخیر"
    LEAVE = "leave", "مرخصی"
