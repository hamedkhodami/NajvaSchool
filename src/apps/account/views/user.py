from django.contrib import messages
from django.contrib.auth import logout
from django.db.models import Q
from django.shortcuts import get_object_or_404, redirect, reverse
from django.views import View
from django.views.generic import DetailView, ListView

from apps.account.enums import UserRoleEnum
from apps.account.mixins import AdminRequiredMixin
from apps.account.models import User
from apps.notification.enums import NotificationTypeEnum
from apps.notification.utils import create_in_app_notification


class UserListView(AdminRequiredMixin, ListView):
    model = User
    template_name = "account/user_list.html"
    context_object_name = "users"

    def get_queryset(self):
        qs = User.objects.all().order_by("-created_at")

        search = self.request.GET.get("search")
        role = self.request.GET.get("role")

        if search:
            qs = qs.filter(
                Q(first_name__icontains=search)
                | Q(last_name__icontains=search)
                | Q(phone_number__icontains=search)
            )

        if role and role in UserRoleEnum.values:
            qs = qs.filter(role=role)

        return qs

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["roles"] = UserRoleEnum.choices
        context["selected_role"] = self.request.GET.get("role", "")
        context["search_value"] = self.request.GET.get("search", "")
        return context


class SendTuitionReminderView(AdminRequiredMixin, View):

    def post(self, request, user_id):
        user = get_object_or_404(User, pk=user_id)

        notification = create_in_app_notification(
            to_user=user,
            notification_type=NotificationTypeEnum.TUITION_REMINDER,
            title="یادآوری پرداخت شهریه",
            description=(
                "کاربر گرامی، لطفاً نسبت به پرداخت شهریه خود اقدام فرمایید. "
                "در صورت عدم پرداخت شهریه در مهلت تعیین‌شده، "
                "دسترسی شما به سامانه طبق مقررات مدرسه به‌صورت خودکار قطع خواهد شد."
            ),
        )

        if notification:
            messages.success(
                request,
                f"اعلان یادآوری شهریه برای {user.full_name} با موفقیت ارسال شد.",
            )
        else:
            messages.error(request, "ارسال اعلان انجام نشد. لطفاً دوباره تلاش کنید.")

        return redirect(
            request.META.get("HTTP_REFERER") or reverse("account:user_list")
        )


class UserDetailView(AdminRequiredMixin, DetailView):
    model = User
    template_name = "account/user_detail.html"
    context_object_name = "user"


class UserAccessToggleView(AdminRequiredMixin, View):
    def post(self, request, user_id):
        user = get_object_or_404(User, id=user_id)

        user.is_active = not user.is_active
        user.save(update_fields=["is_active"])

        if request.user.id == user.id and user.is_active is False:
            logout(request)

        return redirect("account:user_list")
