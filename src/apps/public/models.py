from django.core.exceptions import ValidationError
from django.db import models

from apps.core.models import BaseModel


class AboutUsModel(BaseModel):
    content = models.TextField(
        verbose_name="محتوا",
    )

    image = models.ImageField(
        upload_to="public/about",
        blank=True,
        null=True,
        verbose_name="تصویر",
    )

    class Meta:
        verbose_name = "درباره ما"
        verbose_name_plural = "درباره ما"

    def save(self, *args, **kwargs):
        if not self.pk and AboutUsModel.objects.exists():
            raise ValidationError("تنها یک رکورد درباره ما می‌تواند وجود داشته باشد.")

        super().save(*args, **kwargs)

    def __str__(self):
        return "درباره ما"


class ContactInfoModel(BaseModel):
    phone_number = models.CharField(
        max_length=20,
        verbose_name="شماره تلفن",
    )

    mobile_number = models.CharField(
        max_length=20,
        blank=True,
        verbose_name="شماره موبایل",
    )

    school_number = models.CharField(
        max_length=20,
        blank=True,
        verbose_name="شماره مدرسه",
    )

    address = models.TextField(
        verbose_name="آدرس",
    )

    class Meta:
        verbose_name = "اطلاعات تماس"
        verbose_name_plural = "اطلاعات تماس"

    def save(self, *args, **kwargs):
        if not self.pk and ContactInfoModel.objects.exists():
            raise ValidationError("تنها یک رکورد اطلاعات تماس می‌تواند وجود داشته باشد.")

        super().save(*args, **kwargs)

    def __str__(self):
        return "اطلاعات تماس"


class NewsModel(BaseModel):
    title = models.CharField(
        max_length=200,
        verbose_name="عنوان",
    )

    content = models.TextField(
        verbose_name="محتوا",
    )

    image = models.ImageField(
        upload_to="public/news",
        blank=True,
        null=True,
        verbose_name="تصویر",
    )

    is_published = models.BooleanField(
        default=True,
        verbose_name="منتشر شده",
    )

    published_at = models.DateTimeField(
        null=True,
        blank=True,
        verbose_name="تاریخ انتشار",
    )

    class Meta:
        verbose_name = "خبر"
        verbose_name_plural = "اخبار"
        ordering = ("-published_at", "-created_at")

    def __str__(self):
        return self.title
