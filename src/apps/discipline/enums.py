from django.db.models import TextChoices


class DisciplineEffectEnum(TextChoices):
    POSITIVE = "positive", "مثبت"
    NEGATIVE = "negative", "منفی"


class BehavioralEvaluationLevelEnum(TextChoices):
    EXCELLENT = "excellent", "عالی"
    GOOD = "good", "خوب"
    AVERAGE = "average", "متوسط"
    WEAK = "weak", "ضعیف"


class EducationalRecordTypeEnum(TextChoices):
    CULTURAL = "cultural", "فرهنگی"
    RELIGIOUS = "religious", "مذهبی"
    SPORTS = "sports", "ورزشی"
    SOCIAL = "social", "اجتماعی"
    COMPETITION = "competition", "مسابقه"
    RESPONSIBILITY = "responsibility", "مسئولیت"
    AWARD = "award", "تقدیر"
    OTHER = "other", "سایر"
