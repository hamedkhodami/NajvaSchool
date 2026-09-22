from django.db.models import TextChoices


class NotificationTypeEnum(TextChoices):
    SYSTEM = "system", "سیستمی"
    ADMIN_ALERT = "admin_alert", "اعلان مدیر"
    TUITION_REMINDER = "tuition_reminder", "یادآوری شهریه"
    TUITION_PAYMENT = "tuition_payment", "پرداخت شهریه"
    EDUCATIONAL = "educational", "آموزشی"
    ATTENDANCE = "attendance", "حضور و غیاب"
    DISCIPLINE = "discipline", "انضباطی"
    GENERAL = "general", "عمومی"


class NotificationChannelEnum(TextChoices):
    SMS = "sms", "پیامک"
    IN_APP = "in_app", "داخل سامانه"
    EMAIL = "email", "ایمیل"
