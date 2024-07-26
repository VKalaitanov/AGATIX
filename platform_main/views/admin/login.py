from django.shortcuts import render, HttpResponseRedirect
from django.views import View
from django import forms
from django.http import HttpRequest
from django.contrib.auth import login
from django.core.exceptions import ObjectDoesNotExist

from platform_main.models import User


class LoginForm(forms.Form):
    email = forms.CharField(max_length=100, min_length=3)
    password = forms.CharField(widget=forms.PasswordInput)


class AdminLoginView(View):
    template_name = 'v2/admin/login.html'

    def get(self, request: HttpRequest):
        form = LoginForm()
        return render(request, 'v2/admin/login.html', {'form': form})

    def post(self, request: HttpRequest):
        form = LoginForm(request.POST)
        if form.is_valid():
            try:
                user = User.objects.get(email=form.data['email'])
                password = form.data['password']
                if not user.check_password(password) or not (user.is_admin or user.is_manager):
                    return render(request, 'v2/admin/login.html', {'form': form, 'message': 'User not found'})
            except ObjectDoesNotExist:
                return render(request, 'v2/admin/login.html', {'form': form, 'message': 'User not found'})
        else:
            return render(request, 'v2/admin/login.html', {'form': form})
        login(request, user)
        return HttpResponseRedirect(redirect_to="/admin/home")
