from django.shortcuts import render, reverse
from django.views import View
from django.http import HttpRequest, HttpResponseRedirect, JsonResponse
from django.contrib.auth.mixins import LoginRequiredMixin
from django import forms
from django.views.generic import CreateView, DeleteView

from platform_main.models import SourcePrice, Source
from platform_main.models.enums import Geo
from platform_main.mixins import AdminLoginRequiredMixin, StaffLoginRequiredMixin
from platform_main.utils import clean_form_errors


class UpdatePriceForm(forms.Form):
    price = forms.FloatField(min_value=0)


class AdminSourcesPriceView(StaffLoginRequiredMixin, View):
    @staticmethod
    def get(req: HttpRequest):
        qs = SourcePrice.objects.all().order_by('source__id', 'type', 'format', 'platform', 'geo')
        return render(req,
                      "v2/admin/click_prices.html",
                      {'sources_prices': qs,
                       'sources': Source.objects.all(),
                       'choices_geo': Geo.choices})


class AdminSourcesUpdate(AdminLoginRequiredMixin, View):
    @staticmethod
    def post(req: HttpRequest, source_price: int):
        f = UpdatePriceForm(req.POST)
        if f.is_valid():

            source_price = SourcePrice.objects.get(id=source_price)
            source_price.price = f.data['price']
            source_price.save(update_fields=['price'])
            SourcePrice.objects.filter(source=source_price.source,
                                       type=source_price.type,
                                       format=source_price.format,
                                       platform=source_price.platform).update(price=f.data['price'])
            return JsonResponse({"message": "ok"}, safe=False)
        else:
            return JsonResponse({"message": "errors", "errors": clean_form_errors(f)}, safe=False)


class AdminCreateSourcePrice(AdminLoginRequiredMixin, CreateView):
    model = SourcePrice
    fields = ['source', 'type', 'format', 'platform', 'geo', 'price']
    template_name = 'admin/sources/create_source_price.html'

    def form_valid(self, form):
        obj = form.save()
        return JsonResponse({"message": "ok"}, safe=False)

    def form_invalid(self, form):
        return JsonResponse({"message": "errors", "errors": clean_form_errors(form)}, safe=False)

    def get_success_url(self):
        return reverse('platform_main:admin_sources_prices')


class AdminDeleteSourcePrice(AdminLoginRequiredMixin, DeleteView):
    model = SourcePrice

    def get_success_url(self):
        return reverse('platform_main:admin_sources_prices')
