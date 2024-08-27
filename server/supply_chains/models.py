from datetime import date
from django.db import models
from addresses.models import Address
from inventories.models import InventoryItem
from django.core.validators import EmailValidator, RegexValidator, MinValueValidator


class Supplier(models.Model):
    name = models.CharField(max_length=50, blank=False, null=False)
    email = models.EmailField(
        max_length=100, unique=True, validators=[EmailValidator()], blank=False, null=False)
    phone = models.CharField(max_length=200, validators=[
                             RegexValidator(r'^(\+\d{1,2}\s?)?\(?\d{3}\)?[\s.-]?\d{3}[\s.-]?\d{4}$')], blank=False, null=False)
    address = models.ForeignKey(
        Address, on_delete=models.PROTECT, blank=False, null=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name


class MaterialBySupplier(models.Model):
    raw_material = models.ForeignKey(
        InventoryItem, on_delete=models.PROTECT, blank=False, null=False)
    supplier = models.ForeignKey(
        Supplier, on_delete=models.PROTECT, blank=False, null=False)
    price = models.IntegerField(
        blank=False, null=False, validators=[MinValueValidator(0)])
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f'{self.raw_material.name} by {self.supplier.name}'


class MaterialOrder(models.Model):
    STATUS_CHOICES = [
        ('PEN', 'Pendiente'),
        ('DEL', 'Entregado'),
        ('CAN', 'Cancelado'),
    ]

    status = models.CharField(
        max_length=3, choices=STATUS_CHOICES, default='PEN', blank=False, null=False)
    delivery_date = models.DateField(
        validators=[MinValueValidator(date.today())], blank=False, null=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    @ property
    def total_price(self):
        return sum(detail.partial_price for detail in self.orderdetail_set.all())

    def __str__(self):
        return f'Order {self.pk}'


class OrderDetail(models.Model):
    material_order = models.ForeignKey(
        MaterialOrder, on_delete=models.CASCADE, blank=False, null=False)
    material_by_supplier = models.ForeignKey(
        MaterialBySupplier, on_delete=models.PROTECT, blank=False, null=False)
    quantity = models.IntegerField(blank=False, null=False, validators=[
        MinValueValidator(1)])
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    @ property
    def partial_price(self):
        return self.quantity * self.material_by_supplier.price

    def __str__(self):
        return f'{self.material_by_supplier.raw_material.name} x {self.quantity}'
