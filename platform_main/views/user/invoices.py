from django.http import HttpResponseRedirect, HttpRequest
from django.views.generic import ListView, View
from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.exceptions import ObjectDoesNotExist
from django.views.generic import CreateView
from django.shortcuts import reverse
from django.http import HttpResponse, JsonResponse
from wsgiref.util import FileWrapper
from platform_main.models.invoices import InvoiceTypes
from platform_main.models import Invoice


class ListInvoices(LoginRequiredMixin, ListView):
    template_name = 'v2/user/payments.html'
    context_object_name = 'invoices'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['type_choices'] = InvoiceTypes.choices
        return context

    def get_queryset(self):
        user = self.request.user
        return Invoice.objects.all().filter(user=user, is_deleted=False).order_by('id')


class CreateInvoice(LoginRequiredMixin, CreateView):
    model = Invoice
    fields = ['amount', 'type']
    template_name = 'user/invoices/create.html'

    def form_valid(self, form):
        form.instance.user = self.request.user
        obj = form.save()
        return JsonResponse({"message": "ok"}, safe=False)


class DownloadInvoice(LoginRequiredMixin, View):
    def get(self, req: HttpRequest, invoice_id):
        user = req.user
        try:
            invoice = Invoice.objects.get(id=invoice_id, user=user)
        except ObjectDoesNotExist:
            return HttpResponseRedirect(reverse('platform_main:user_invoices_list'))
        content = FileWrapper(invoice.generate_pdf())
        response = HttpResponse(content, content_type='application/pdf')
        response['Content-Disposition'] = 'attachment; filename=invoice # %s.pdf' % str(invoice_id)
        return response
