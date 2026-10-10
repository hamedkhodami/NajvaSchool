from django.contrib.auth.mixins import UserPassesTestMixin
from django.core.exceptions import PermissionDenied

from apps.account.enums import UserRoleEnum


class TeacherRequiredMixin(UserPassesTestMixin):
    def test_func(self):
        user = self.request.user
        return (
            user.is_authenticated
            and getattr(user, "role", None) == UserRoleEnum.TEACHER
        )

    def handle_no_permission(self):
        raise PermissionDenied("اجازه‌ی ورود به این صفحه را ندارید.")


class TeacherOrAdminRequiredMixin(UserPassesTestMixin):
    def test_func(self):
        user = self.request.user

        if not user.is_authenticated:
            return False

        is_teacher = getattr(user, "role", None) == UserRoleEnum.TEACHER
        is_admin = getattr(user, "role", None) == UserRoleEnum.ADMIN or getattr(
            user, "is_admin", False
        )

        return is_teacher or is_admin

    def handle_no_permission(self):
        raise PermissionDenied("فقط معلمان و مدیران اجازه‌ی ورود به این بخش را دارند.")
