from django.db.models import TextChoices


class StudentStatusEnum(TextChoices):
    ACTIVE = "active", "فعال"
    INACTIVE = "inactive", "غیرفعال"
    GRADUATED = "graduated", "فارغ‌التحصیل"
    TRANSFERRED = "transferred", "انتقال‌یافته"
    SUSPENDED = "suspended", "معلق"
