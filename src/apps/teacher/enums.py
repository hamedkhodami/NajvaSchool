from django.db.models import TextChoices


class TeacherStatusEnum(TextChoices):
    ACTIVE = "active", "فعال"
    INACTIVE = "inactive", "غیرفعال"
    ON_LEAVE = "on_leave", "در مرخصی"
    SUSPENDED = "suspended", "معلق"
    TERMINATED = "terminated", "پایان همکاری"


class EmploymentTypeEnum(TextChoices):
    FULL_TIME = "full_time", "تمام‌وقت"
    PART_TIME = "part_time", "پاره‌وقت"
    CONTRACT = "contract", "قراردادی"
    TEMPORARY = "temporary", "موقت"
