from django.contrib.auth.mixins import UserPassesTestMixin
from django.core.exceptions import PermissionDenied

from apps.account.enums import UserRoleEnum


class StudentRequiredMixin(UserPassesTestMixin):
    def test_func(self):
        user = self.request.user
        return (
            user.is_authenticated
            and getattr(user, "role", None) == UserRoleEnum.STUDENT
        )

    def handle_no_permission(self):
        raise PermissionDenied("فقط دانش‌آموزان اجازه‌ی ورود به این صفحه را دارند.")
