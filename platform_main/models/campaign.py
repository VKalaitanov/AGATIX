from django.db import models
from django.db.models import OuterRef, F, Sum, ExpressionWrapper, Value, Min
from django.db.models.functions import Coalesce
from django.utils import timezone
from django.utils.translation import gettext_lazy as _
from django.core.exceptions import ObjectDoesNotExist
from django.contrib.postgres.fields import ArrayField
from django import forms

from platform_main.models.enums import Geo, EmailType, OperationalSystem, Platform, Format
from utils.models import ModelEnhanced


class ChoiceArrayField(ArrayField):
    """
    A field that allows us to store an array of choices.

    Uses Django 1.9's postgres ArrayField
    and a MultipleChoiceField for its formfield.

    Usage:

        choices = ChoiceArrayField(models.CharField(max_length=...,
                                                    choices=(...,)),
                                   default=[...])
    """

    def formfield(self, **kwargs):
        defaults = {
            'form_class': forms.MultipleChoiceField,
            'choices': self.base_field.choices,
        }
        defaults.update(kwargs)
        # Skip our parent's formfield implementation completely as we don't
        # care for it.
        # pylint:disable=bad-super-call
        return super(ArrayField, self).formfield(**defaults)


class Status(models.TextChoices):
    RUNNING = 'running', _('Running')
    STOPPED = 'stopped', _('Stopped')


class FutureStatuses(models.TextChoices):
    REQUEST_STOP = 'stop_requested', _("Stop requested")
    REQUEST_RUN = 'run_requested', _("Run requested")


FutureStatusesMapping = {
    FutureStatuses.REQUEST_STOP.value: Status.STOPPED.value,
    FutureStatuses.REQUEST_RUN.value: Status.RUNNING.value
}


class Source(ModelEnhanced):
    name = models.CharField(max_length=20)
    system_id = models.CharField(max_length=20, unique=True)

    def __str__(self):
        return self.name


class SourcePrice(ModelEnhanced):
    source = models.ForeignKey(Source, on_delete=models.CASCADE)
    type = models.CharField(choices=EmailType.choices)
    format = models.CharField(choices=Format.choices)
    platform = models.CharField(choices=Platform.choices)
    geo = models.CharField(choices=Geo.choices)
    price = models.DecimalField(max_digits=10, decimal_places=4)

    @classmethod
    def get_unique_values(cls, filter_data: dict):
        return cls.objects.all().filter(**filter_data) \
            .order_by() \
            .values('source', 'type', 'format', 'platform', 'geo')

    @classmethod
    def get_min_price(cls, filter_data: dict):
        res = cls.objects.all().filter(**filter_data).aggregate(min_price=Min('price'))
        return res.get('min_price', 0)


class CustomCampaignManager(models.Manager):
    def get_queryset(self):
        return super().get_queryset().filter(is_deleted=False)

    def get_sources_statistics(self):
        subquery_utils = {k: OuterRef(k) for k in ['format', 'type', 'geo', 'os', 'platform', 'source']}
        subquery_running = self.get_queryset() \
            .filter(current_status=Status.RUNNING.value, **subquery_utils) \
            .values('format', 'type', 'geo', 'platform', 'source') \
            .annotate(total_clicks=Sum('clicks_per_day', default=0)) \
            .values('total_clicks')
        subquery_waiting_for_moderation = self.get_queryset() \
            .filter(current_status=Status.STOPPED.value, next_status__isnull=False, **subquery_utils) \
            .values('format', 'type', 'geo', 'platform', 'source') \
            .annotate(total_clicks=Sum('clicks_per_day', default=0)) \
            .values('total_clicks')
        res = self.get_queryset().values('format', 'type', 'geo', 'platform', 'source__id', 'source__name') \
            .annotate(current=Coalesce(subquery_running, Value(0))) \
            .annotate(future=Coalesce(subquery_waiting_for_moderation, F('current'))) \
            .annotate(delta=ExpressionWrapper(F('future') - F('current'), output_field=models.IntegerField()))
        res = res.distinct()
        return res


class Campaign(ModelEnhanced):
    name = models.CharField(max_length=250)
    type = models.CharField(choices=EmailType.choices)
    format = models.CharField(choices=Format.choices)
    link = models.CharField(max_length=250)
    platform = models.CharField(choices=Platform.choices)
    os = ChoiceArrayField(base_field=models.CharField(choices=OperationalSystem.choices, max_length=20), null=False)
    geo = models.CharField(choices=Geo.choices)
    price = models.DecimalField(max_digits=10, decimal_places=4)
    # daily_budget = models.IntegerField(null=True)
    clicks_per_day = models.IntegerField()
    user = models.ForeignKey('platform_main.User', on_delete=models.SET_NULL, related_name='campaigns', null=True)
    current_status = models.CharField(choices=Status.choices, default=Status.STOPPED)
    next_status = models.CharField(choices=FutureStatuses.choices, null=True)
    is_deleted = models.BooleanField(default=False)
    source = models.ForeignKey('platform_main.Source', on_delete=models.PROTECT)

    @property
    def os_display(self):
        return ', '.join([str(OperationalSystem(_os).label) for _os in self.os])

    def moderation_decision(self, action: str):
        if action == 'start':
            next_status = Status.RUNNING.value
        elif action == 'stop':
            next_status = Status.STOPPED.value
        else:
            raise Exception
        self.next_status = None
        self.current_status = next_status
        self.save(update_fields=['current_status', 'next_status'])

    def user_action(self, action: FutureStatuses):
        next_status = FutureStatusesMapping.get(action.value)
        if next_status == self.current_status:
            self.next_status = None
            self.save(update_fields=['next_status'])
        else:
            self.next_status = action.value
            self.save(update_fields=['next_status'])

    def delete(self, *args, **kwargs):
        self.is_deleted = True
        self.save(update_fields=['is_deleted'])

    @property
    def get_css_class(self):
        match self.current_status:
            case "running":
                return "start"
            case "stopped":
                return "stop"

    @property
    def get_button_src(self):
        match self.current_status:
            case "running":
                return f"admin/campaigns/stop.svg"
            case "stopped":
                return f"admin/campaigns/start.svg"

    @property
    def clicks_today(self) -> int:
        try:
            clicks = self.clicks_set.all().get(at=timezone.now().replace(minute=0, second=0, microsecond=0))
            return clicks.clicks
        except ObjectDoesNotExist:
            return 0

    objects = CustomCampaignManager()
