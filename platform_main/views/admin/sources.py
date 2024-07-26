from django.shortcuts import render, reverse
from django.views import View
from django.http import HttpRequest, JsonResponse
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import CreateView, UpdateView, DeleteView, TemplateView

from platform_main.models import Campaign, Format, EmailType, Geo, Platform, Source
from platform_main.mixins import AdminLoginRequiredMixin, StaffLoginRequiredMixin
from platform_main.utils import clean_form_errors


class AdminSourcesView(StaffLoginRequiredMixin, TemplateView):
    template_name = 'v2/admin/sources.html'

    def get_sources_statistics(self):
        sources_statistics = Campaign.objects.get_sources_statistics()
        for s in sources_statistics:
            s['format'] = Format(s['format']).label
            s['type'] = EmailType(s['type']).label
            s['geo'] = (s['geo'], Geo(s['geo']).label)
            s['platform'] = Platform(s['platform']).label
        return sources_statistics

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["sources_statistics"] = self.get_sources_statistics()
        context["sources"] = Source.objects.all().order_by('id')
        return context


class AdminCreateSource(AdminLoginRequiredMixin, CreateView):
    model = Source
    fields = ['name', 'system_id']
    template_name = 'admin/sources/create_source.html'

    def form_valid(self, form):
        obj = form.save()
        return JsonResponse({'message': "ok"}, safe=False)

    def form_invalid(self, form):
        return JsonResponse({'message': "errors", "errors": clean_form_errors(form)}, safe=False)


class AdminUpdateSource(AdminLoginRequiredMixin, UpdateView):
    model = Source
    fields = ['name', 'system_id']
    template_name = 'admin/sources/update_source.html'

    def form_valid(self, form):
        obj = form.save()
        return JsonResponse({'message': "ok"}, safe=False)

    def form_invalid(self, form):
        return JsonResponse({'message': "errors", "errors": clean_form_errors(form)}, safe=False)


class AdminDeleteSource(AdminLoginRequiredMixin, DeleteView):
    model = Source
    template_name = 'admin/sources/delete_source.html'

    def get_success_url(self):
        return reverse('platform_main:admin_sources_list')
