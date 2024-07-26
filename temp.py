import os
import django
from django.conf import settings
from datetime import datetime

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'redirectplatform.settings')
django.setup()
# from platform_main.celery_tasks import get_tasks_from_integration
from platform_main.models import Campaign, Clicks

if __name__ == '__main__':
    campaign = Campaign.objects.get(id=1)
    clicks, _ = Clicks.objects.get_or_create(campaign=campaign, at=datetime.now())
    clicks.clicks = 10
    clicks.save(update_fields=['clicks'])
