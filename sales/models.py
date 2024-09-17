from django.db import models
from django.contrib.auth import get_user_model
from products.models import (
    Carpet,
    CustomOptionDetail,
)


class PayMethod(models.Model):
    name = models.CharField(max_length=50, unique=True,
                            blank=False, null=False)

    def __str__(self):
        return self.name


class DeliveryMethod(models.Model):
    name = models.CharField(max_length=50, unique=True,
                            blank=False, null=False)
    price = models.PositiveIntegerField(blank=False, null=False, default=0)

    def __str__(self):
        return self.name


class Sale(models.Model):
    user = models.ForeignKey(get_user_model(), on_delete=models.CASCADE)
    pay_method = models.ForeignKey(PayMethod, on_delete=models.PROTECT)
    delivery_method = models.ForeignKey(
        DeliveryMethod, on_delete=models.PROTECT)
    date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'{self.user} - {self.date}'

    @ property
    def total_price(self):
        carpet_price = sum(
            detail.partial_price for detail in self.saledetail_set.all())
        delivery_price = self.delivery_method.price
        return carpet_price + delivery_price


class SaleDetail(models.Model):
    sale = models.ForeignKey(
        Sale, on_delete=models.CASCADE, related_name='items')
    carpet = models.ForeignKey(Carpet, on_delete=models.PROTECT)
    quantity = models.PositiveIntegerField()

    @ property
    def partial_price(self):
        carpet_price = self.quantity * self.carpet.price
        option_price = sum(
            option.total_price for option in self.saledetailoption_set.all())
        return carpet_price + option_price


class SaleDetailOption(models.Model):
    sale_detail = models.ForeignKey(
        SaleDetail, on_delete=models.CASCADE, related_name='options')
    custom_option_detail = models.ManyToManyField(
        CustomOptionDetail, blank=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    @ property
    def total_price(self):
        return sum(detail.price for detail in self.custom_option_detail.all())
