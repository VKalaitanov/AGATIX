import calendar
from datetime import datetime, timezone, timedelta
from django.db.models.functions import TruncDay
from django.db.models import F, Sum


def filter_qs(qs, value: str):
    dt_from, dt_upto = None, None
    now = datetime.now(tz=timezone.utc)
    match value:
        case "Last month":
            now = now.replace(day=1) - timedelta(days=2)
            dt_from = now.replace(day=1, hour=0, minute=0, second=0, microsecond=0)
            dt_upto = now.replace(day=calendar.monthrange(now.year, now.month)[1], hour=23, minute=59, second=59)

        case "Current month":
            dt_from = now.replace(day=1, hour=0, minute=0, second=0, microsecond=0)
            dt_upto = now.replace(day=calendar.monthrange(now.year, now.month)[1], hour=23, minute=59, second=59)
            print(dt_from,dt_upto)
        case "Last week":
            now = now - timedelta(days=now.weekday() + 7)
            dt_from = now.replace(hour=0, minute=0, second=0, microsecond=0)
            dt_upto = (dt_from + timedelta(days=6)).replace(hour=23, minute=59, second=59)

        case "Current week":
            now = now - timedelta(days=now.weekday())
            dt_from = now.replace(hour=0, minute=0, second=0, microsecond=0)
            dt_upto = (dt_from + timedelta(days=6)).replace(hour=23, minute=59, second=59)
        case "Today":
            dt_from = now.replace(hour=0, minute=0, second=0, microsecond=0)
            dt_upto = now.replace(hour=23, minute=59, second=59)
        case "Yesterday":
            now -= timedelta(days=1)
            dt_from = now.replace(hour=0, minute=0, second=0, microsecond=0)
            dt_upto = now.replace(hour=23, minute=59, second=59)
        case _:
            pass
    if dt_from:
        qs = qs.filter(at__gte=dt_from)
    if dt_upto:
        qs = qs.filter(at__lte=dt_upto)

    return qs
