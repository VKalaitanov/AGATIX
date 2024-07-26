from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import reverse


class AdminLoginRequiredMixin(LoginRequiredMixin):
    def get_login_url(self):
        return reverse('platform_main:admin_login')

    def dispatch(self, request, *args, **kwargs):
        if not request.user.is_authenticated or not request.user.is_admin:
            return self.handle_no_permission()
        return super().dispatch(request, *args, **kwargs)


class StaffLoginRequiredMixin(LoginRequiredMixin):
    def get_login_url(self):
        return reverse('platform_main:admin_login')

    def dispatch(self, request, *args, **kwargs):
        if not request.user.is_authenticated or not (request.user.is_admin or request.user.is_manager):
            return self.handle_no_permission()
        return super().dispatch(request, *args, **kwargs)
