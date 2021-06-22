from django.db import models
from apps.base.models import BaseModel


class TestModel(BaseModel):
    """ Some model for the tests. """

    name = models.CharField(max_length=50, blank=True)
    address = models.CharField(max_length=50, blank=True)
    price = models.DecimalField(
        decimal_places=2,
        max_digits=8,
        blank=True
    )


class TestModel2(BaseModel):
    """ Some model for the tests. """

    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    address = models.CharField(max_length=50)
    price = models.DecimalField(decimal_places=0, max_digits=8)
    reciever = models.ForeignKey(TestModel, on_delete=models.CASCADE)