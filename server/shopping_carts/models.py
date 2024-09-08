from django.db import models
from django.contrib.auth import get_user_model
from django.core.validators import MinValueValidator
from products.models import Carpet, CustomOptionDetail


class ShoppingCart(models.Model):
    user = models.ForeignKey(get_user_model(), on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    @property
    def total_price(self):
        return sum(detail.partial_price for detail in self.shoppingcartitem_set.all())


class ShoppingCartItem(models.Model):
    shopping_cart = models.ForeignKey(
        ShoppingCart, on_delete=models.CASCADE, blank=False, null=False)
    carpet = models.ForeignKey(
        Carpet, on_delete=models.CASCADE, blank=False, null=False)
    quantity = models.IntegerField(blank=False, null=False, validators=[
        MinValueValidator(1)])
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    @property
    def partial_price(self):
        carpet_price = self.quantity * self.carpet.price
        option_price = sum(
            option.total_price for option in self.shoppingcartitemoption_set.all())
        return carpet_price + option_price


class ShoppingCartItemOption(models.Model):
    shopping_cart_item = models.ForeignKey(
        ShoppingCartItem, on_delete=models.CASCADE, blank=False, null=False)
    custom_option_detail = models.ManyToManyField(
        CustomOptionDetail, blank=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    @ property
    def total_price(self):
        return sum(detail.price for detail in self.custom_option_detail.all())
