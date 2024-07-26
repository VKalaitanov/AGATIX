import json

from django.http import HttpResponseRedirect, HttpRequest
from django.views.generic import ListView, View
from django.core.exceptions import ObjectDoesNotExist
from django.shortcuts import reverse
from django.http import HttpResponse, JsonResponse
from wsgiref.util import FileWrapper

from platform_main.models import Invoice, Status
from platform_main.mixins import AdminLoginRequiredMixin, StaffLoginRequiredMixin
from platform_main.models.invoices import InvoiceTypes


class AdminListInvoices(StaffLoginRequiredMixin, ListView):
    template_name = 'v2/admin/invoices.html'
    context_object_name = 'invoices'

    def get_queryset(self):
        queryset = Invoice.objects.all()

        form_name = self.request.GET.get('name')
        form_status = self.request.GET.get('status')
        form_type = self.request.GET.get('type')

        if form_name:
            if form_name.isdigit():
                queryset = queryset.filter(id=form_name)
            else:
                queryset = queryset
        if form_status:
            queryset = queryset.filter(paid=int(form_status))
        if form_type:
            queryset = queryset.filter(type=form_type)

        return queryset.order_by('-created_at')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['choices_status'] = [('0', 'Waiting'), ('1', 'Paid')]
        context['choices_type'] = InvoiceTypes.choices
        return context





class AdminInvoiceAccept(AdminLoginRequiredMixin, View):
    @staticmethod
    def post(req: HttpRequest, pk: int):
        try:
            invoice = Invoice.objects.get(id=pk)
        except ObjectDoesNotExist:
            return JsonResponse({"message": "notfound", "errors": "invoice not found"}, safe=False, status=404)
        status = json.loads(req.body)['status']
        if status == 'run':
            invoice.paid = True
            invoice.save(update_fields=['paid'])
            invoice.user.edit_balance(invoice.amount)
        elif status == 'wait':
            invoice.paid = False
            invoice.save(update_fields=['paid'])
            invoice.user.balance -= invoice.amount
            invoice.user.save(update_fields=['balance'])

        return JsonResponse({"message": "ok"}, safe=False)

    @staticmethod
    def get(req: HttpRequest, pk: int):
        return HttpResponseRedirect(reverse('platform_main:admin_list_invoices'))


class AdminInvoiceDelete(AdminLoginRequiredMixin, View):
    @staticmethod
    def post(req: HttpRequest, pk: int):
        try:
            invoice = Invoice.objects.get(id=pk)
        except ObjectDoesNotExist:
            return HttpResponseRedirect(reverse('platform_main:admin_list_invoices'))
        invoice.is_deleted = True
        invoice.save(update_fields=['is_deleted'])
        return HttpResponseRedirect(reverse('platform_main:admin_list_invoices'))

    @staticmethod
    def get(req: HttpRequest, pk: int):
        return HttpResponseRedirect(reverse('platform_main:admin_list_invoices'))


class AdminDownloadInvoice(StaffLoginRequiredMixin, View):
    def get(self, req: HttpRequest, pk):
        try:
            invoice = Invoice.objects.get(id=pk)
        except ObjectDoesNotExist:
            return HttpResponseRedirect(reverse('platform_main:admin_list_invoices'))
        content = FileWrapper(invoice.generate_pdf())
        response = HttpResponse(content, content_type='application/pdf')
        response['Content-Disposition'] = 'attachment; filename=invoice # %s.pdf' % str(pk)
        return response
