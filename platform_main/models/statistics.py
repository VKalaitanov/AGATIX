from django.db import models
from django.contrib.auth.models import AbstractBaseUser, UserManager, PermissionsMixin
from platform_main.models.campaign import Status

from utils.models import ModelEnhanced


class Statistics(ModelEnhanced):
    date = models.DateField()
    clicks = models.IntegerField(default=0)
    company = models.ForeignKey('platform_main.Campaign', on_delete=models.CASCADE)
