from django.urls import path

from apps.notification.views import PendingNotificationsView, UserNotificationListView


app_name = "notification"

urlpatterns = [
    path("my/", UserNotificationListView.as_view(), name="user_notifications"),
    path(
        "pending/",
        PendingNotificationsView.as_view(),
        name="pending_notifications",
    ),
]
