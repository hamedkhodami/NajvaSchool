from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import redirect, render
from django.views import View

from apps.core.pagination import paginate_queryset
from apps.notification.models import Notification


class UserNotificationListView(LoginRequiredMixin, View):

    def get(self, request):
        notifications = Notification.objects.filter(
            to_user=request.user,
            is_showing=True,
        ).order_by("-created_at", "-id")

        pagination = paginate_queryset(
            request=request,
            queryset=notifications,
            per_page=10,
        )

        return render(
            request,
            "notification/user_notifications.html",
            {
                "notifications": pagination["object_list"],
                "paginator": pagination["paginator"],
                "page_obj": pagination["page_obj"],
                "is_paginated": pagination["is_paginated"],
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
