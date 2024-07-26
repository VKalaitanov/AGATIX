from django.http import HttpResponseRedirect
from django.core.exceptions import ObjectDoesNotExist
from django.contrib.auth import login, logout
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views import View
from django.shortcuts import reverse, redirect

from rest_framework.renderers import TemplateHTMLRenderer
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.views import APIView

from platform_main.models import User
from platform_main.views.user.serializer import UserSerializer, LoginSerializer


class LoginView(APIView):
    template_name = 'v2/auth/login.html'
    renderer_classes = [TemplateHTMLRenderer]

    def get(self, request: Request):
        user = request.user
        if user.is_authenticated:
            return HttpResponseRedirect(redirect_to="/home")
        return Response({'serializer': LoginSerializer()})

    def post(self, request: Request):
        data = request.data
        serializer = LoginSerializer(data=data)
        if not serializer.is_valid():
            return Response({'serializer': serializer, 'message': 'Invalid credentials'})
        try:
            user = User.objects.get(email=serializer.validated_data['email'], is_admin=False)
        except ObjectDoesNotExist:
            return Response({'serializer': serializer, 'message': 'User not found'})
        if not user.check_password(serializer.validated_data['password']):
            return Response({'serializer': serializer, 'message': 'Invalid password'})
        login(request, user)
        return HttpResponseRedirect(redirect_to="/home/")


class HomeView(LoginRequiredMixin, APIView):
    template_name = "v2/user/index.html"
    renderer_classes = [TemplateHTMLRenderer]

    def get(self, request: Request):
        user = request.user
        return Response(UserSerializer(user).data)


class LogoutView(View):
    @staticmethod
    def get(request: Request):
        logout(request)
        return HttpResponseRedirect(reverse('platform_main:login'))


def home_redirect(request):
    return redirect('platform_main:login')
