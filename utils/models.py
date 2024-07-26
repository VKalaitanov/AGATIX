from django.db import models


class TimestampMixin:
    created_at = models.DateTimeField(auto_now=True)
    edited_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        abstract = True


class ModelEnhanced(models.Model, TimestampMixin):
    id = models.BigAutoField(primary_key=True, editable=False)

    class Meta:
        abstract = True
