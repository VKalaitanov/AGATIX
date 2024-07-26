from django.shortcuts import render, HttpResponseRedirect
from django.views import View
from django.urls import reverse
from django import forms
from django.http import HttpRequest, JsonResponse

from django.db.models import Q
from django.core.exceptions import ObjectDoesNotExist
from django.views.generic import ListView

from platform_main.models import User
from platform_main.mixins import AdminLoginRequiredMixin, StaffLoginRequiredMixin
from platform_main.utils import clean_form_errors


class AccountForm(forms.ModelForm):
    email = forms.CharField(widget=forms.TextInput(attrs={'readonly': 'readonly'}))

    def __init__(self, *args, **kwargs):
        super(AccountForm, self).__init__(*args, **kwargs)
        self.fields['manager'].queryset = User.objects.filter(Q(is_admin=True) | Q(is_manager=True))

    class Meta:
        model = User
        fields = ['email', 'name', 'manager', 'company', 'balance', 'allow_zero_balance']


class AccountForAdminForm(AccountForm):
    class Meta:
        model = User
        fields = ['email', 'name', 'manager', 'company', 'balance', 'allow_zero_balance', 'is_admin', 'is_manager']


class AdminAccountsView(StaffLoginRequiredMixin, ListView):
    template_name = 'v2/admin/accounts.html'
    context_object_name = 'accounts'

    def get_queryset(self):
        user: User = self.request.user
        if not user.is_admin:
            return User.objects.filter(manager=user).order_by('id')
        return User.objects.all().filter(is_admin=False, is_manager=False).order_by('id')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['managers'] = User.objects.filter(is_manager=True)
        return context


class AdminDeleteAccountView(AdminLoginRequiredMixin, View):
    @staticmethod
    def post(req: HttpRequest, account_id: str):
        try:
            user = User.objects.get(id=account_id)
            user.delete()
        except ObjectDoesNotExist:
            pass
        return HttpResponseRedirect(reverse('platform_main:admin_accounts_list'))


class AdminAccountView(StaffLoginRequiredMixin, View):
    @staticmethod
    def get(req: HttpRequest, account_id: str):
        user: User = req.user
        try:
            if not user.is_admin:
                account = User.objects.get(id=account_id, manager=user)
                form = AccountForm
            else:
                account = User.objects.get(id=account_id)
                form = AccountForAdminForm
        except ObjectDoesNotExist:
            return HttpResponseRedirect(reverse('platform_main:admin_accounts_list'))
        form = form(instance=account)
        return render(req, 'admin/get_account.html', {'form': form, 'id': account_id})

    @staticmethod
    def post(req: HttpRequest, account_id: str):
        user: User = req.user
        try:
            if not user.is_admin:
                account = User.objects.get(id=account_id, manager=user)
                form = AccountForm
            else:
                account = User.objects.get(id=account_id)
                form = AccountForAdminForm
        except ObjectDoesNotExist:
            return JsonResponse({"message": "errors"}, safe=False, status=404)
            # return HttpResponseRedirect(reverse('platform_main:admin_accounts_list'))
        form = form(req.POST, instance=account)
        if form.is_valid():
            form.save()
            return JsonResponse({"message": "ok"}, safe=False)
        else:
            return JsonResponse({"message": "errors", "errors": clean_form_errors(form)}, safe=False)
        # return render(req, 'admin/get_account.html', {'form': form, 'id': account_id})


class AdminStopAccount(StaffLoginRequiredMixin, View):
    @staticmethod
    def post(req: HttpRequest, account_id: str):
        try:
            account = User.objects.get(id=account_id)
        except ObjectDoesNotExist:
            return HttpResponseRedirect(reverse('platform_main:admin_accounts_list'))
        account.stop()
        return HttpResponseRedirect(reverse('platform_main:admin_accounts_list'))
