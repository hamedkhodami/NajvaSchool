from apps.notification.email_handlers import EmailHandlers
from apps.notification.enums import NotificationChannelEnum
from apps.notification.inapp_handlers import InAppHandlers


class NotificationDispatcher:

    @staticmethod
    def dispatch(notification):
        channel = notification.channel
        user = notification.to_user

        if channel == NotificationChannelEnum.SMS:
            NotificationDispatcher._dispatch_sms(notification, user.phone_number)

        elif channel == NotificationChannelEnum.EMAIL:
            NotificationDispatcher._dispatch_email(notification)

        elif channel == NotificationChannelEnum.IN_APP:
            NotificationDispatcher._dispatch_inapp(notification)

    @staticmethod
    def _dispatch_sms(notification, phone_number):
        handlers = {}

        handler = handlers.get(notification.type)
        if handler:
            handler(notification, phone_number)

    @staticmethod
    def _dispatch_email(notification):
        EmailHandlers.send_email(notification)

    @staticmethod
    def _dispatch_inapp(notification):
        InAppHandlers.create_inapp(notification)
