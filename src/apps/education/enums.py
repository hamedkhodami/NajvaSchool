from django.db.models import TextChoices


class AssignmentStatusEnum(TextChoices):
    PENDING = "pending", "در انتظار"
    SUBMITTED = "submitted", "تحویل داده شده"
    REVIEWED = "reviewed", "بررسی شده"
    LATE = "late", "با تأخیر"


class EducationalActivityTypeEnum(TextChoices):
    TEACHING = "teaching", "تدریس"
    REVIEW = "review", "مرور"
    EXERCISE = "exercise", "حل تمرین"
    QUESTIONING = "questioning", "پرسش"
    GROUP_WORK = "group_work", "کار گروهی"
    OTHER = "other", "سایر"
