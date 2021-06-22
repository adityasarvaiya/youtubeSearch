from django.db import models
from safedelete.models import SafeDeleteModel, SOFT_DELETE_CASCADE

from apps.base.managers import SoftDeleteManager, SoftDeleteAllManager


class TimestampedModel(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True


class SoftDeleteModel(SafeDeleteModel):
    """
    Managers over-written to allow performance improvements in case of bulk hard-delete
    """

    _safedelete_policy = SOFT_DELETE_CASCADE

    objects = SoftDeleteManager()
    all_objects = SoftDeleteAllManager()

    class Meta:
        abstract = True


class BaseModel(SoftDeleteModel, TimestampedModel):

    class Meta:
        abstract = True