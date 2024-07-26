from django.db import models


class Clicks(models.Model):
    at = models.DateTimeField()
    clicks = models.IntegerField(default=0)
    campaign = models.ForeignKey('platform_main.Campaign', on_delete=models.PROTECT, null=True)
    amount = models.IntegerField(default=0)

    def set_clicks(self, clicks: int):
        self.clicks = clicks
        self.save(update_fields=['clicks'])

    def set_amount(self, delta: int):
        self.amount += delta
        self.save(update_fields=['delta'])
