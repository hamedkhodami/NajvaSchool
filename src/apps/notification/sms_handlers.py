from apps.core.utils import send_sms


class SMSHandlers:

    @staticmethod
    def mobile_verification(notification, phone_number):
        pattern = ""  # کد پترن OTP
        send_sms(
            phone_number,
            pattern,
            **{"verification-code": notification.kwargs["code"]},
        )
