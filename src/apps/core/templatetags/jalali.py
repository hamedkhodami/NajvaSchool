from datetime import date, datetime

from django import template
from khayyam import JalaliDate, JalaliDatetime


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


def jalali_to_gregorian(j_year, j_month, j_day):
    return JalaliDate(j_year, j_month, j_day).todate()


def gregorian_to_jalali(g_date: date):
    return JalaliDate(g_date)


def jalali_days_in_month(year, month):
    if 1 <= month <= 6:
        return 31
    if 7 <= month <= 11:
        return 30
    return 30 if JalaliDate(year, 12, 1).isleap() else 29


def today_jalali():
    return JalaliDate.today()


def today_gregorian():
    return JalaliDate.today().todate()
