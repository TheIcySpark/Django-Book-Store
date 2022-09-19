import datetime

from django.db import models
from django.contrib.auth.models import User


class BookModel(models.Model):
    title = models.CharField(max_length=100)
    editorial = models.CharField(max_length=100)
    author = models.CharField(max_length=100)
    year = models.DateField()
    edition = models.CharField(max_length=50)
    city = models.CharField(max_length=100)
    stock = models.IntegerField(default=1)
    price = models.FloatField(default=1)


class UserPurchaseHistoryModel(models.Model):
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        null=True,
        blank=True
    )
    book = models.ForeignKey(
        BookModel,
        on_delete=models.CASCADE,
        null=True,
        blank=True,
    )
    date = models.DateField(default=datetime.date.today)
    qty = models.IntegerField(blank=True, null=True, default=None)
    price = models.FloatField(blank=True, null=True, default=None)


class ProfileDataModel(models.Model):
    user = models.OneToOneField(
        User,
        on_delete=models.CASCADE,
        primary_key=True,
    )
    country = models.CharField(max_length=250, blank=True, null=True, default=None)
    city = models.CharField(max_length=200, blank=True, null=True, default=None)
    address = models.CharField(max_length=250, blank=True, null=True, default=None)
    zip_or_postal_code = models.IntegerField(blank=True, null=True, default=None)
    phone = models.IntegerField(blank=True, null=True, default=None)
    book_coins = models.FloatField(default=0, blank=True, null=True)
