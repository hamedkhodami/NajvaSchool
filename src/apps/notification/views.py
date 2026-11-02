from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.paginator import Paginator
from django.shortcuts import redirect, render
from django.views import View

from apps.notification.models import Notification


class UserNotificationListView(LoginRequiredMixin, View):
    def get(self, request):
        notifications = Notification.objects.filter(
            to_user=request.user,
            is_showing=True,
        ).order_by("-created_at")

        paginator = Paginator(notifications, 10)
        page_obj = paginator.get_page(request.GET.get("page"))

        return render(
            request,
            "notification/user_notifications.html",
            {
                "notifications": page_obj.object_list,
                "page_obj": page_obj,
            },
        )


class PendingNotificationsView(LoginRequiredMixin, View):
    template_name = "notification/pending_notifications.html"

    def get(self, request):
        notifications = Notification.objects.filter(
            to_user=request.user,
            is_showing=True,
            is_read=False,
        ).order_by("-created_at")

        if not notifications.exists():
            return redirect("dashboard")

        return render(
            request,
            self.template_name,
            {"notifications": notifications},
        )

    def post(self, request):
        Notification.objects.filter(
            to_user=request.user,
            is_showing=True,
            is_read=False,
        ).update(is_read=True)

        return redirect("dashboard:dashboard")
