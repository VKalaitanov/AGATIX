from django.db import models
from django.contrib.auth.models import AbstractBaseUser, UserManager, PermissionsMixin
from platform_main.models.campaign import Status, FutureStatuses

from utils.models import ModelEnhanced


class CustomUserManager(UserManager):
    def get_queryset(self):
        return super().get_queryset().filter(is_deleted=False)


class User(ModelEnhanced, AbstractBaseUser, PermissionsMixin):
    email = models.CharField(max_length=100, unique=True)
    name = models.CharField(max_length=100, unique=True)
    manager = models.ForeignKey('platform_main.User', null=True, on_delete=models.SET_NULL)
    company = models.CharField(max_length=255, null=True, blank=True)
    balance = models.DecimalField(max_digits=10, decimal_places=4, default=0)
    is_deleted = models.BooleanField(default=False)
    is_admin = models.BooleanField(default=False)
    is_manager = models.BooleanField(default=False)
    is_stopped = models.BooleanField(default=False)
    allow_zero_balance = models.BooleanField(default=False)

    objects = CustomUserManager()

    def edit_balance(self, delta):
        self.balance += delta
        self.save(update_fields=['balance'])

    @property
    def clicks_per_day_total(self):
        campaigns = self.campaigns.all().filter(is_deleted=False, current_status=Status.RUNNING.value)
        return sum([c.clicks_per_day for c in campaigns])

    @property
    def is_staff(self):
        return self.is_admin

    @classmethod
    def create_user(cls, email: str, password: str, name: str = None):
        user = cls(email=email)
        if name is not None:
            user.name = name
        user.set_password(password)
        user.save()
        user.refresh_from_db()
        return user

    @property
    def pretty_balance(self):
        full = str(self.balance).split('.')
        first = full[0]
        second = full[1]
        result = first + '.' + second[:2]
        return result

    def stop(self):
        self.is_stopped = not self.is_stopped
        self.save(update_fields=['is_stopped'])
        if self.is_stopped:
            running_campaigns = self.campaigns.all().filter(current_status=Status.RUNNING.value)
            stopped_campaigns = self.campaigns.all().filter(next_status__isnull=False)
            running_campaigns.update(current_status=Status.STOPPED.value, next_status=FutureStatuses.REQUEST_RUN.value)
            stopped_campaigns.update(current_status=Status.STOPPED.value, next_status=None)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username']

    def delete(self, *args, **kwargs):
        self.is_deleted = True
        self.campaigns.all().update(is_deleted=True)
        self.save(update_fields=['is_deleted'])

    def is_admin_or_manager(self):
        return self.is_admin or self.is_manager
