from django.db.models import TextChoices


class PaymentMethodEnum(TextChoices):
    CASH = "cash", "نقدی"
    CARD_TO_CARD = "card_to_card", "کارت به کارت"
    GATEWAY = "gateway", "درگاه پرداخت"


class PaymentStatusEnum(TextChoices):
    PENDING = "pending", "در انتظار"
    PAID = "paid", "پرداخت شده"
    FAILED = "failed", "ناموفق"
    CANCELLED = "cancelled", "لغو شده"


class TuitionStatusEnum(TextChoices):
    PENDING = "pending", "در انتظار پرداخت"
    PARTIAL = "partial", "پرداخت ناقص"
    PAID = "paid", "تسویه شده"
    CANCELLED = "cancelled", "لغو شده"


class SalaryStatusEnum(TextChoices):
    PENDING = "pending", "در انتظار پرداخت"
    PARTIAL = "partial", "پرداخت ناقص"
    PAID = "paid", "پرداخت شده"


class ExpenseCategoryEnum(TextChoices):
    SALARY = "salary", "حقوق"
    EQUIPMENT = "equipment", "تجهیزات"
    MAINTENANCE = "maintenance", "تعمیرات"
    UTILITIES = "utilities", "قبوض و خدمات"
    EDUCATION = "education", "آموزشی"
    OFFICE = "office", "اداری"
    TRANSPORTATION = "transportation", "حمل‌ونقل"
    OTHER = "other", "سایر"


class IncomeCategoryEnum(TextChoices):
    TUITION = "tuition", "شهریه"
    DONATION = "donation", "کمک و مشارکت"
    OTHER = "other", "سایر"


class FinancialReportTypeEnum(TextChoices):
    TUITION = "tuition", "شهریه"
    SALARY = "salary", "حقوق"
    EXPENSE = "expense", "هزینه"
    INCOME = "income", "درآمد"
    GENERAL = "general", "گزارش کلی"
