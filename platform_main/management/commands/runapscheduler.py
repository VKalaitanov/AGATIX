import logging
from datetime import timedelta, datetime
from apscheduler.schedulers.blocking import BlockingScheduler
from apscheduler.executors.pool import ThreadPoolExecutor, ProcessPoolExecutor
from apscheduler.triggers.interval import IntervalTrigger
from apscheduler.util import undefined
from django_apscheduler.jobstores import DjangoJobStore
from django.utils import timezone
from django.core.management.base import BaseCommand
from django.conf import settings

from platform_main.celery_tasks import get_tasks_from_integration

logger = logging.getLogger(__name__)

_job_defaults = {
    'coalesce': False,
    'max_instances': 3,
}
_timezone = settings.TIME_ZONE
_executors = {
    'default': ThreadPoolExecutor(10),
    'processpool': ProcessPoolExecutor(4),
}
scheduler = BlockingScheduler(
    jobstores={'default': DjangoJobStore()},
    job_defaults=_job_defaults,
    executors=_executors,
    timezone=_timezone,
)

RUN_IMMEDIATELY = True

dt = timezone.now()


def next_run():
    return dt if RUN_IMMEDIATELY else undefined


class PreviouslessIntervalTrigger(IntervalTrigger):
    def get_next_fire_time(self, previous_fire_time, now):
        return super().get_next_fire_time(None, now)


class Command(BaseCommand):
    help = "Runs APScheduler."

    def handle(self, *args, **options):
        p = timedelta(seconds=30)
        scheduler.add_job(
            get_tasks_from_integration, id="run_integration", replace_existing=True, max_instances=1,
            trigger=PreviouslessIntervalTrigger(seconds=int(p.total_seconds()),
                                                start_date=datetime(year=dt.year, month=dt.month, day=dt.day,
                                                                    tzinfo=dt.tzinfo)),
            coalesce=False, misfire_grace_time=None, next_run_time=next_run(),
        )
        try:
            logger.info("Starting scheduler...")
            scheduler.start()
        except KeyboardInterrupt:
            logger.info("Stopping scheduler...")
            scheduler.shutdown()
            logger.info("Scheduler shut down successfully!")
