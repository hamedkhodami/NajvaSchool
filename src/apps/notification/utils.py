from apps.account.models import User
from apps.notification.enums import (
    NotificationChannelEnum,
)
from apps.notification.models import Notification
from apps.notification.services.dispatcher import NotificationDispatcher


def create_notify_for_admins(type, title):
    admins = User.objects.filter(is_admin=True)
    for admin in admins:
        Notification.objects.create(type=type, to_user=admin, title=title)


def create_in_app_notification(
    *,
    to_user,
    notification_type,
    title,
    description="",
    link="",
):
    """
    ساخت و ارسال اعلان درون‌برنامه‌ای
    """

    if not to_user:
        return None

    notification = Notification.objects.create(
        type=notification_type,
        channel=NotificationChannelEnum.IN_APP,
        title=title,
        description=description,
        kwargs={"link": link} if link else {},
        to_user=to_user,
        send_notify=True,
    )

    NotificationDispatcher.dispatch(notification)

    return notification
