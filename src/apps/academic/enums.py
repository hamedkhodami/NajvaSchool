from django.db.models import TextChoices


class AcademicYearStatusEnum(TextChoices):
    PLANNED = "planned", "در حال برنامه‌ریزی"
    ACTIVE = "active", "فعال"
    COMPLETED = "completed", "پایان‌یافته"


class ClassroomStatusEnum(TextChoices):
    ACTIVE = "active", "فعال"
    INACTIVE = "inactive", "غیرفعال"
    COMPLETED = "completed", "پایان‌یافته"


class EnrollmentStatusEnum(TextChoices):
    ACTIVE = "active", "فعال"
    COMPLETED = "completed", "تکمیل‌شده"
    CANCELLED = "cancelled", "لغوشده"
    TRANSFERRED = "transferred", "انتقال‌یافته"


class WeekDayEnum(TextChoices):
    SATURDAY = "saturday", "شنبه"
    SUNDAY = "sunday", "یکشنبه"
    MONDAY = "monday", "دوشنبه"
    TUESDAY = "tuesday", "سه‌شنبه"
    WEDNESDAY = "wednesday", "چهارشنبه"
    THURSDAY = "thursday", "پنجشنبه"
    FRIDAY = "friday", "جمعه"
