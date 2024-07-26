import requests
from datetime import datetime, timezone, timedelta
from platform_main.models import Campaign, Clicks


def get_tasks_from_integration():
    d = (datetime.now(tz=timezone.utc) - timedelta(minutes=5)).replace(minute=0, second=0, microsecond=0)
    url = "http://localhost:1337/clicks_statistics"
    response = requests.get(url, data={'at': d.isoformat()})
    if response.status_code != 200:
        print('Error | Status code,', response.status_code)
        return

    data = response.json()
    failed_clicks = data.pop('failed')
    inst, created = Clicks.objects.get_or_create(campaign=None, at=d)
    inst.set_clicks(failed_clicks)
    print(f"{failed_clicks} failed clicks")

    for key, value in data.items():
        print(f'key = {key}, value = {value}')
        campaign = Campaign.objects.get(id=key)
        inst, created = Clicks.objects.get_or_create(campaign=campaign, at=d)
        if inst.clicks < value:
            user = campaign.user
            user.edit_balance(-(value - inst.clicks) * campaign.price)
            inst.set_clicks(value)
            inst.set_amount((value - inst.clicks) * campaign.price)
