import calendar
import datetime
import json
from datetime import datetime, timedelta

import pytz
from django.http import HttpResponseRedirect, HttpRequest, JsonResponse
from django.views.generic import ListView, View, UpdateView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.exceptions import ObjectDoesNotExist, ValidationError
from django.db.models import Q, Sum
from django.shortcuts import render, reverse
from django import forms

from platform_main.models import Campaign, Status, FutureStatuses, User, Clicks, Platform, DesktopOS, MobileOS, \
    OperationalSystem, SourcePrice, EmailType, Format, Geo, Source
from utils.qs_functions import filter_qs
from platform_main.utils import clean_form_errors


class CreateCampaignFormStageOne(forms.ModelForm):
    start_after_moderation = forms.BooleanField(required=False)
    fields_update_on_change = ["type", "format", "geo", "source"]
    enums_mapping = {
        'type': EmailType,
        'format': Format,
        'geo': Geo,
        'platform': Platform
    }

    class Meta:
        model = Campaign
        fields = [
            "name",
            "link",
            "source",
            "type",
            "format",
            "geo",
            "platform",
            "start_after_moderation"
        ]

    def specify_values(self):
        instance = self.instance
        query = {}
        for field in self.fields_update_on_change:
            try:
                value = getattr(instance, field)
                if value:
                    query[field] = value
            except ObjectDoesNotExist:
                continue
        if source_id := self.data.get('source'):
            query['source__id'] = source_id
        unique_values = SourcePrice.get_unique_values(query)
        values = {f: [] for f in self.fields_update_on_change}
        for price in unique_values:
            for field in self.fields_update_on_change:
                values[field].append(price[field])

        for field in self.fields_update_on_change:
            form_field = self.fields.get(field)
            form_field.widget.attrs = {'onchange': 'form.submit();'}
            if field != 'source':
                form_field.choices = [
                    (self.enums_mapping[field](v).value, self.enums_mapping[field](v).label) for v in set(values[field])
                ]
            else:
                form_field.queryset = Source.objects.all()

        price = SourcePrice.get_min_price(query)
        if field := self.fields.get('price'):
            field.widget.attrs['min'] = price
            field.widget.attrs['placeholder'] = price


class CreateCampaignFormStageTwo(CreateCampaignFormStageOne):
    os = forms.MultipleChoiceField(
        widget=forms.CheckboxSelectMultiple,
        choices=OperationalSystem.choices,
    )

    class Meta:
        model = Campaign
        fields = [
            "name",
            "link",
            "source",
            "type",
            "format",
            "geo",
            "platform",
            "start_after_moderation",
            "os",
            "clicks_per_day",
            "price",
        ]

    def os_choices(self, platform: str):

        match platform:
            case Platform.MOBILE.value:
                self.fields.get('os').choices = MobileOS.choices
            case Platform.DESKTOP.value:
                self.fields.get('os').choices = DesktopOS.choices
            case _:
                self.fields.get('os').choices = OperationalSystem.choices

    def clean_price(self):
        price = self.cleaned_data['price']
        query = {}
        for field in self.fields_update_on_change:
            value = self.cleaned_data.get(field)
            if value:
                query[field] = value
        if source := self.cleaned_data.get('source'):
            query['source'] = source
        min_price = SourcePrice.get_min_price(query)

        if price < min_price:
            raise ValidationError(f' ')
        return price


class CreateCampaignView(LoginRequiredMixin, View):
    last_stage_fields = ["os", "clicks_per_day", "price"]

    def get(self, request: HttpRequest):
        form = CreateCampaignFormStageOne()
        form.specify_values()
        return render(request,
                      "campaigns/create.html",
                      {
                          'form': form
                      })

    def post(self, request: HttpRequest):
        data = request.POST
        platform = data.get('platform')
        if platform is None:
            form = CreateCampaignFormStageOne(data=data)
        else:
            form = CreateCampaignFormStageTwo(data=data)
            form.os_choices(platform)
        form.specify_values()

        if any([data.get(f) is None for f in self.last_stage_fields]) or not form.is_valid():
            return JsonResponse({"message": "errors", "errors": clean_form_errors(form)}, safe=False)

        campaign: Campaign = form.instance
        campaign.user = request.user
        if campaign.user.balance:
            campaign.next_status = FutureStatuses.REQUEST_RUN.value
        campaign.save()
        return JsonResponse({"message": "ok"}, safe=False)
        # return HttpResponseRedirect(redirect_to="/campaigns/list")

def get_min_price(request):
    values = json.loads(request.body)
    prices = SourcePrice.objects.filter(platform=values['platform'], source=values['source'],geo=values['geo'],type=values['type'], format=values['format'])
    try:
        min_price=min([i.price for i in prices])
    except:
        min_price=0
    return JsonResponse({'min_price': min_price})


class ListCampaignsView(LoginRequiredMixin, ListView):
    template_name = 'v2/user/campaigns.html'
    context_object_name = 'campaigns'

    def get_queryset(self):
        user = self.request.user
        queryset = Campaign.objects.all().filter(user=user).order_by('id')
        form_type = self.request.GET.get('type')
        form_geo = self.request.GET.get('geo')
        form_os = self.request.GET.get('os')
        form_status = self.request.GET.get('status')
        form_name = self.request.GET.get('name')


        if form_name:
            if form_name.isdigit():
                queryset = queryset.filter(id=form_name)
            else:
                queryset = queryset.filter(name__icontains=form_name)
        if form_os:
            queryset = queryset.filter(os=[form_os])
        if form_type:
            queryset = queryset.filter(type=form_type)
        if form_geo:
            queryset = queryset.filter(geo=form_geo)
        if form_status:
            queryset = queryset.filter(current_status=form_status)

        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        form = CreateCampaignFormStageOne()
        form.specify_values()
        context['sources'] = Source.objects.all()
        context['choices_geo'] = Geo.choices
        context['choices_os'] = OperationalSystem.choices
        context['choices_status'] = Status.choices
        context['choices_type'] = EmailType.choices
        context['form'] = form
        return context


class CampaignAction(LoginRequiredMixin, View):
    def post(self, req: HttpRequest, campaign_id: str, action: str):
        user: User = req.user
        if action == FutureStatuses.REQUEST_STOP.value:
            try:
                campaign = Campaign.objects.get(Q(current_status=Status.RUNNING.value) |
                                                Q(current_status=Status.STOPPED.value), id=campaign_id, user=user)
            except ObjectDoesNotExist:
                pass
            else:
                campaign.user_action(FutureStatuses.REQUEST_STOP)
        elif action == FutureStatuses.REQUEST_RUN.value:
            try:
                campaign = Campaign.objects.get(Q(current_status=Status.RUNNING.value) |
                                                Q(current_status=Status.STOPPED.value), id=campaign_id, user=user)
            except ObjectDoesNotExist:
                pass
            else:
                campaign.user_action(FutureStatuses.REQUEST_RUN)

        return HttpResponseRedirect(redirect_to="/campaigns/list")


class CampaignStatistics(LoginRequiredMixin, View):
    def get(self, req: HttpRequest, campaign_id: str):
        statistics_by = req.GET.get('statistics_by')
        try:
            campaign = Campaign.objects.get(id=campaign_id)
        except ObjectDoesNotExist:
            return HttpResponseRedirect(redirect_to="/campaigns/list")

        qs = filter_qs(campaign.clicks_set.all().order_by('at'), statistics_by)
        total_clicks = qs.aggregate(total_clicks=Sum('clicks'))['total_clicks']

        total_amount = qs.aggregate(total_amount=Sum('amount'))['total_amount']

        return render(req,
                      "v2/user/statistics.html",
                      {
                          'clicks': qs,
                          'total_clicks': total_clicks if total_clicks != None else 0,
                          'total_amount': total_amount if total_amount != None else 0,
                          'campaign_id': campaign_id
                      })


class AllStatistics(LoginRequiredMixin, View):
    def get(self, req: HttpRequest):
        return render(req,
                      "v2/admin/statistics.html",
                      )


def get_statistic(request):
    date_range = request.GET.get('date_range', 'Today')
    if request.user.is_anonymous or request.user.is_admin or request.user.is_manager:
        clicks = Clicks.objects.all()
    else:
        campaigns = Campaign.objects.filter(user=request.user)
        clicks = Clicks.objects.all().filter(campaign__in=campaigns)

    if date_range == 'Today':
        start_date = datetime.now().date()
        end_data = start_date +timedelta(days=1)
        labels = [(start_date + timedelta(days=i)).strftime("%d %B") for i in range(1)]
        clicks = clicks.filter(at__range=(start_date, end_data))
        clicks_per_period = [
            clicks.filter(campaign__current_status='running').aggregate(sc=Sum('clicks'))['sc']]
        clicks_per_period = list(map(lambda x: x if x is not None else 0, clicks_per_period))
        failed_clicks = [
            clicks.filter(campaign__current_status='stopped').aggregate(
                sc=Sum('clicks'))['sc']]
        failed_clicks_per_period = list(map(lambda x: x if x is not None else 0, failed_clicks))

    elif date_range == 'Yesterday':
        start_date = datetime.now().date() - timedelta(days=1)
        end_data = start_date + timedelta(days=1)
        labels = [(start_date + timedelta(days=i)).strftime("%d %B") for i in range(1)]
        clicks = clicks.filter(at__range=(start_date, end_data))
        clicks_per_period = [
            clicks.filter(campaign__current_status='running').aggregate(sc=Sum('clicks'))['sc']]
        clicks_per_period = list(map(lambda x: x if x is not None else 0, clicks_per_period))
        failed_clicks = [
            clicks.filter(campaign__current_status='stopped').aggregate(
                sc=Sum('clicks'))['sc']]
        failed_clicks_per_period = list(map(lambda x: x if x is not None else 0, failed_clicks))
    elif date_range == 'Current week':
        today = datetime.now().date()
        start_date = today - timedelta(days=today.weekday())
        end_date = start_date + timedelta(days=6)
        labels = [(start_date + timedelta(days=i)).strftime("%d %B %a") for i in range(7)]
        clicks = clicks.filter(at__range=(start_date, end_date))
        clicks_per_period = [
            clicks.filter(at__day=(start_date + timedelta(days=i)).day, campaign__current_status='running').aggregate(sc=Sum('clicks'))['sc'] for i in
            range(7)]
        clicks_per_period = list(map(lambda x: x if x is not None else 0, clicks_per_period))

        failed_clicks = [clicks.filter(at__day=(start_date + timedelta(days=i)).day, campaign__current_status='stopped').aggregate(sc=Sum('clicks'))['sc'] for i in
            range(7)]
        failed_clicks_per_period = list(map(lambda x: x if x is not None else 0, failed_clicks))

    elif date_range == 'Last week':
        today = datetime.now().date()
        start_date = today - timedelta(days=today.weekday() + 7)
        end_date = start_date + timedelta(days=6)
        labels = [(start_date + timedelta(days=i)).strftime("%d %B %a") for i in range(7)]
        clicks = clicks.filter(at__range=(start_date, end_date))
        clicks_per_period = [
            clicks.filter(at__day=(start_date + timedelta(days=i)).day, campaign__current_status='running').aggregate(sc=Sum('clicks'))['sc'] for i in
            range(7)]
        clicks_per_period = list(map(lambda x: x if x is not None else 0, clicks_per_period))
        failed_clicks = [
            clicks.filter(at__day=(start_date + timedelta(days=i)).day, campaign__current_status='stopped').aggregate(
                sc=Sum('clicks'))['sc'] for i in
            range(7)]
        failed_clicks_per_period = list(map(lambda x: x if x is not None else 0, failed_clicks))

    elif date_range == 'Current month':
        today = datetime.now().date()
        start_date = datetime(today.year, today.month, 1)
        end_date = start_date + timedelta(days=32)
        end_date = end_date.replace(day=1) - timedelta(days=1)
        days_in_month = calendar.monthrange(today.year, today.month)[1]

        labels = [(start_date + timedelta(days=i)).strftime("%d/%m/%Y") for i in range(days_in_month)]
        clicks = clicks.filter(at__range=(start_date, end_date))
        clicks_per_period = [
            clicks.filter(at__day=(start_date + timedelta(days=i)).day, campaign__current_status = 'running').aggregate(sc=Sum('clicks'))['sc'] for i in
            range(days_in_month)]
        clicks_per_period = list(map(lambda x: x if x is not None else 0, clicks_per_period))
        failed_clicks = [
            clicks.filter(at__day=(start_date + timedelta(days=i)).day, campaign__current_status='stopped').aggregate(
                sc=Sum('clicks'))['sc'] for i in
            range(days_in_month)]
        failed_clicks_per_period = list(map(lambda x: x if x is not None else 0, failed_clicks))

    elif date_range == 'Last month':
        today = datetime.now().date()
        start_date = datetime(today.year, today.month, 1) - timedelta(days=1)
        start_date = start_date.replace(day=1)
        end_date = datetime(today.year, today.month, 1) - timedelta(days=1)
        days_in_month = calendar.monthrange(start_date.year, start_date.month)[1]
        labels = [(start_date + timedelta(days=i)).strftime("%d/%m/%Y") for i in range(days_in_month)]
        clicks = clicks.filter(at__range=(start_date, end_date))
        clicks_per_period = [
            clicks.filter(at__day=(start_date + timedelta(days=i)).day, campaign__current_status='running').aggregate(sc=Sum('clicks'))['sc'] for i in
            range(days_in_month)]
        clicks_per_period = list(map(lambda x: x if x is not None else 0, clicks_per_period))
        failed_clicks = [
            clicks.filter(at__day=(start_date + timedelta(days=i)).day, campaign__current_status='stopped').aggregate(
                sc=Sum('clicks'))['sc'] for i in
            range(days_in_month)]
        failed_clicks_per_period = list(map(lambda x: x if x is not None else 0, failed_clicks))

    data = {
        'total_clicks': clicks.filter(campaign__current_status='running').aggregate(sc=Sum('clicks'))['sc'],
        'total_amount': clicks.filter(campaign__current_status='running').aggregate(sa=Sum('amount'))['sa'],
        'failed_total_clicks': clicks.filter(campaign__current_status='stopped').aggregate(sc=Sum('clicks'))['sc'],
        'failed_total_amount': clicks.filter(campaign__current_status='stopped').aggregate(sa=Sum('amount'))['sa'],

        'data': {'labels': labels, 'clicks': clicks_per_period, 'failed_clicks': failed_clicks_per_period}
    }
    return JsonResponse(data)


class DeleteCampaign(LoginRequiredMixin, View):
    def post(self, req: HttpRequest, pk: int):
        user = req.user
        try:
            campaign = Campaign.objects.get(id=pk, user=user, current_status=Status.STOPPED)
            campaign.delete()
        except ObjectDoesNotExist:
            pass
        finally:
            return HttpResponseRedirect(redirect_to="/campaigns/list")


class UpdateCampaign(LoginRequiredMixin, UpdateView):
    model = Campaign
    fields = ['name', 'link', 'clicks_per_day']
    template_name = 'campaigns/edit.html'

    def get_object(self, queryset=None):
        user = self.request.user
        pk = self.kwargs.get(self.pk_url_kwarg)
        campaign = Campaign.objects.get(id=pk, user=user)
        return campaign

    def form_valid(self, form):
        obj = form.save()
        return JsonResponse({"message": "ok"}, safe=False)

    def form_invalid(self, form):
        print(form)
        errors = clean_form_errors(form)
        return JsonResponse({"message": "errors", "errors": errors}, safe=False)
