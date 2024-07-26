from typing import Literal
from itertools import chain

from django.shortcuts import render, HttpResponseRedirect
from django.views import View
from django.urls import reverse
from django import forms
from django.http import HttpRequest, JsonResponse
from django.core.exceptions import ObjectDoesNotExist
from django.views.generic import ListView, UpdateView
from django.db.models import Sum

from platform_main.models import Campaign, Status, Source, Clicks, User, EmailType
from platform_main.mixins import AdminLoginRequiredMixin, StaffLoginRequiredMixin
from utils.qs_functions import filter_qs
from platform_main.utils import clean_form_errors


class SourceMCF(forms.ModelChoiceField):
    def label_from_instance(self, source: Source):
        return f"{source.name}"


class CampaignForm(forms.ModelForm):
    source = SourceMCF(queryset=Source.objects.all())

    class Meta:
        model = Campaign
        fields = ['name', 'type', 'format', 'link', 'platform', 'os', 'geo', 'price', 'clicks_per_day', 'user',
                  'source']


class AdminHomeView(StaffLoginRequiredMixin, View):
    template_name = 'v2/admin/campaigns.html'

    @staticmethod
    def get(req: HttpRequest):
        return render(req, "v2/admin/index.html")


class AdminCreateCampaignView(StaffLoginRequiredMixin, View):
    template_name = 'v2/admin/campaigns.html'

    @staticmethod
    def get(req: HttpRequest):
        return render(req, "v2/admin/campaigns.html", {"form": CampaignForm()})

    @staticmethod
    def post(req: HttpRequest):
        form = CampaignForm(data=req.POST)
        if not form.is_valid():
            return JsonResponse({"message": "errors", "errors": clean_form_errors(form)}, safe=False)
            # return render(req, 'admin/campaigns/create_campaign.html', {'form': form})
        form.save()
        return JsonResponse({"message": "ok"}, safe=False)


class AdminCampaignsView(StaffLoginRequiredMixin, ListView):
    template_name = 'v2/admin/campaigns.html'
    context_object_name = 'campaigns'

    def get_queryset(self):
        status_filter = self.request.GET.get('status')
        queryset = Campaign.objects.all()

        form_name = self.request.GET.get('name')
        form_email = self.request.GET.get('email_search')
        form_status = self.request.GET.get('status')
        form_type = self.request.GET.get('type')



        if form_name:
            if form_name.isdigit():
                queryset = queryset.filter(id=form_name)
            else:
                queryset = queryset.filter(name__icontains=form_name)
        if form_email:
            queryset = queryset.filter(user__email__icontains=form_email)
        if form_status:
            queryset = queryset.filter(current_status=form_status)
        if form_type:
            queryset = queryset.filter(type=form_type)


        return queryset.order_by('id')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['users'] = User.objects.filter(is_admin=False, is_manager=False)
        context['create_campaign'] = CampaignForm()
        context['choices_status'] = Status.choices
        context['choices_type'] = EmailType.choices
        return context


class AdminDeleteCampaignView(StaffLoginRequiredMixin, View):
    @staticmethod
    def post(req: HttpRequest, campaign_id: str):
        try:
            campaign = Campaign.objects.get(id=campaign_id)
            campaign.delete()
        except ObjectDoesNotExist:
            pass
        return HttpResponseRedirect(reverse('platform_main:admin_campaigns_list'))


class AdminCampaign(StaffLoginRequiredMixin, View):
    @staticmethod
    def get(req: HttpRequest, campaign_id: str):
        try:
            campaign = Campaign.objects.get(id=campaign_id)
        except ObjectDoesNotExist:
            return HttpResponseRedirect(reverse('platform_main:admin_campaigns_list'))
        return render(req, "admin/campaigns/update_campaign.html",
                      {"form": CampaignForm(instance=campaign), "id": campaign_id})

    @staticmethod
    def post(req: HttpRequest, campaign_id: str):
        try:
            campaign = Campaign.objects.get(id=campaign_id)
        except ObjectDoesNotExist:
            return HttpResponseRedirect(reverse('platform_main:admin_campaigns_list'))
        form = CampaignForm(req.POST, instance=campaign)
        if form.is_valid():
            form.save()
        return render(req, 'admin/get_account.html', {'form': form, 'id': campaign_id})


class AdminCampaignUpdate(StaffLoginRequiredMixin, UpdateView):
    model = Campaign
    fields = ['name', 'link', 'clicks_per_day']
    template_name = 'campaigns/edit.html'
    pk_url_kwarg = 'campaign_id'

    def get_object(self, queryset=None):
        user = self.request.user
        pk = self.kwargs.get(self.pk_url_kwarg)
        campaign = Campaign.objects.get(id=pk)
        return campaign

    def form_invalid(self, form):
        return JsonResponse({"message": "errors", "errors": clean_form_errors(form)}, safe=False)

    def form_valid(self, form):
        obj = form.save()
        return JsonResponse({"message": "ok"}, safe=False)

    def get_success_url(self):
        return reverse('platform_main:admin_campaigns_list')


class AdminCampaignAction(StaffLoginRequiredMixin, View):
    action: Literal['start', 'stop'] = None

    def post(self, req: HttpRequest, campaign_id: str):
        try:
            campaign = Campaign.objects.get(id=campaign_id)
        except ObjectDoesNotExist:
            return HttpResponseRedirect(reverse('platform_main:admin_campaigns_list'))
        campaign.moderation_decision(self.action)
        return HttpResponseRedirect(reverse('platform_main:admin_campaigns_list'))


class TotalStatistics(StaffLoginRequiredMixin, View):
    def get(self, req: HttpRequest):
        active_clicks = Clicks.objects.all().filter(campaign__isnull=False) \
            .values('at') \
            .order_by('at') \
            .annotate(clicks=Sum('clicks'))
        statistics_by = req.GET.get('statistics_by')
        qs = filter_qs(active_clicks, statistics_by)
        failed_qs = filter_qs(Clicks.objects.all().filter(campaign__isnull=True), statistics_by).values('at', 'clicks')
        success_clicks = {}
        failed_clicks = {}
        for click in qs:
            success_clicks[click['at']] = click['clicks']
        for click in failed_qs:
            failed_clicks[click['at']] = click['clicks']
        clicks = []
        for at in sorted(set(chain(qs.values_list('at', flat=True), failed_qs.values_list('at', flat=True)))):
            clicks.append((at, success_clicks.get(at, 0), failed_clicks.get(at, 0)))

        return render(req,
                      "admin/total_statistics.html",
                      {
                          'clicks': clicks,

                      })
