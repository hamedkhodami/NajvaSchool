from django.contrib.auth import get_user_model
from django.db import models

from apps.core.models import BaseModel
from apps.notification.enums import (
    NotificationChannelEnum,
    NotificationTypeEnum,
)


User = get_user_model()


class Notification(BaseModel):
    Type = NotificationTypeEnum
    Channel = NotificationChannelEnum

    type = models.CharField(
        max_length=50,
        choices=Type.choices,
        verbose_name="نوع اعلان",
    )

    channel = models.CharField(
        max_length=50,
        choices=Channel.choices,
        default=NotificationChannelEnum.IN_APP,
        verbose_name="کانال ارسال",
    )

    title = models.CharField(
        max_length=255,
        verbose_name="عنوان اعلان",
    )

    description = models.TextField(
        blank=True,
        null=True,
        verbose_name="متن اعلان",
    )

    kwargs = models.JSONField(
        blank=True,
        null=True,
        verbose_name="اطلاعات اضافی",
    )

    send_notify = models.BooleanField(
        default=True,
        verbose_name="ارسال اعلان",
    )

    to_user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name="notifications",
        verbose_name="گیرنده",
    )

    is_showing = models.BooleanField(
        default=True,
        verbose_name="نمایش اعلان",
    )

    class Meta:
        verbose_name = "اعلان"
        verbose_name_plural = "اعلان‌ها"
        ordering = ("-created_at",)

    def __str__(self):
        return f"{self.to_user} - {self.title}"

    def get_title(self):
        return self.title or "اعلان"

    def get_content(self):
        return f"""
            {self.get_title()}
            {self.description or ""}
        """

    def get_link(self):
        if not self.kwargs:
            return ""

        return self.kwargs.get("link", "")
