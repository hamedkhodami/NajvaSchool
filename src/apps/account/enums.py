from django.db.models import TextChoices


class UserRoleEnum(TextChoices):
    ADMIN = "admin", "ادمین"
    TEACHER = "teacher", "معلم"
    STUDENT = "student", "دانش‌آموز"
