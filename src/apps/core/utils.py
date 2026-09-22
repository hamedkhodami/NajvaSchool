import os
from os.path import splitext
import uuid

from django.contrib import messages
from django.utils import timezone
from django.utils.translation import gettext as _


def get_timesince_persian(time):
    if not time:
        return ""

    diff = timezone.now() - time

    seconds = int(diff.total_seconds())

    intervals = (
        (31536000, _("years ago")),
        (2592000, _("months ago")),
        (86400, _("days ago")),
        (3600, _("hours ago")),
        (60, _("minutes ago")),
    )

    for interval_seconds, label in intervals:
        value = seconds // interval_seconds

        if value:
            return f"{value} {label}"

    return _("Moments ago")


# Get time in format
def get_time(frmt: str = "%Y-%m-%d %H:%M"):
    now = timezone.now()
    if frmt is not None:
        now = now.strftime(frmt)

    return now


# Create image/file path based on time
def upload_file_src(instance, filename):
    now = timezone.now()
    _, extension = os.path.splitext(filename)
    extension = extension.lower()
    unique_name = f"{uuid.uuid4()}{extension}"
    return f"files/{now.year}/{now.month:02d}/{unique_name}"


# Return file extension
def get_file_extension(file_name):
    return splitext(str(file_name))[-1].lower()


# Form validator utils
def validate_form(request, form):
    if form.is_valid():
        return True

    errors = form.errors.items()

    if not errors:
        messages.error(request, _("Entered data is not correct."))
        return False

    for field, message in errors:  # noqa: B007
        for error in message:
            messages.error(request, error)

    return False


# Toast form errors utils
def toast_form_errors(request, form):
    errors = form.errors.items()
    if not errors:
        messages.error(request, _("Entered data is not correct."))
        return False

    for field, message in errors:  # noqa: B007
        for error in message:
            messages.error(request, error)
            return False


def send_sms(request):
    pass
