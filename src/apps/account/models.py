from datetime import timedelta

from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin
from django.db import models
from django.utils import timezone

from apps.account.enums import UserRoleEnum
from apps.account.managers import UserManager
from apps.core.models import BaseModel


class User(BaseModel, AbstractBaseUser, PermissionsMixin):
    Role = UserRoleEnum

    phone_number = models.CharField("شماره موبایل", max_length=11, unique=True)
    first_name = models.CharField("نام", max_length=128, null=True, blank=True)
    last_name = models.CharField("نام خانوادگی", max_length=128, null=True, blank=True)

    role = models.CharField(
        "نقش", max_length=128, choices=Role.choices, default=Role.STUDENT
    )

    is_active = models.BooleanField("فعال", default=True)
    is_admin = models.BooleanField("ادمین", default=False)
    is_verified = models.BooleanField("تأیید شده", default=False)

    objects = UserManager()

    USERNAME_FIELD = "phone_number"
    REQUIRED_FIELDS = []

    class Meta:
        verbose_name = "کاربر"
        verbose_name_plural = "کاربران"

    def __str__(self):
        return self.phone_number

    @property
    def full_name(self):
        return f"{self.first_name or ''} {self.last_name or ''}".strip() or "بدون نام"

    def last_login_within(self, days):
        if self.last_login:
            local_time = timezone.localtime(self.last_login)
            return local_time >= timezone.now() - timedelta(days=days)
        return False

    @property
    def is_staff(self):
        return self.is_superuser or self.is_admin
