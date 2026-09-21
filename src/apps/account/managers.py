from django.contrib.auth.models import BaseUserManager

from apps.account.enums import UserRoleEnum


class UserManager(BaseUserManager):
    def create_user(self, phone_number, password=None, **extra_fields):
        if not phone_number:
            raise ValueError("شماره موبایل الزامی است")

        extra_fields.setdefault("role", UserRoleEnum.STUDENT)
        extra_fields.setdefault("is_active", True)
        extra_fields.setdefault("is_verified", False)
        extra_fields.setdefault("is_admin", False)

        user = self.model(phone_number=phone_number, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, phone_number, password=None, **extra_fields):

        extra_fields.setdefault("role", UserRoleEnum.ADMIN)
        extra_fields.setdefault("is_admin", True)
        extra_fields.setdefault("is_superuser", True)
        extra_fields.setdefault("is_active", True)
        extra_fields.setdefault("is_verified", True)

        return self.create_user(
            phone_number=phone_number, password=password, **extra_fields
        )
