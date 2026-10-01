from datetime import date, datetime

from django import template
from khayyam import JalaliDatetime


register = template.Library()


@register.filter
def jalali(value, arg=None):
    try:
        if not value:
            return ""

        if isinstance(value, date) and not isinstance(value, datetime):
            value = datetime.combine(value, datetime.min.time())

        if isinstance(value, str):
            try:
                value = datetime.fromisoformat(value)
            except:
                return value

        format_string = arg if arg else "%Y/%m/%d"

        return JalaliDatetime(value).strftime(format_string)

    except Exception:
        return value
