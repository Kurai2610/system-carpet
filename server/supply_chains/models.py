from django.db import models
from addresses.models import Address
from inventories.models import InventoryItem
from django.core.validators import EmailValidator, RegexValidator

# Create your models here.


class Supplier(models.Model):
    name = models.CharField(max_length=200)
    email = models.EmailField(
        max_length=200, unique=True, validators=[EmailValidator()])
    phone = models.CharField(max_length=200, validators=[
                             RegexValidator(r'^\+?1?\d{9,15}$')])
    address = models.ForeignKey(Address, on_delete=models.PROTECT)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name


class RawMaterial(models.Model):
    inventory_item = models.OneToOneField(
        InventoryItem, on_delete=models.PROTECT)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.inventory_item.name


class MaterialBySupplier(models.Model):
    raw_material = models.ForeignKey(RawMaterial, on_delete=models.PROTECT)
    supplier = models.ForeignKey(Supplier, on_delete=models.PROTECT)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f'{self.raw_material.inventory_item.name} by {self.supplier.name}'


class MaterialOrder(models.Model):
    total_price = models.DecimalField(max_digits=10, decimal_places=2)
    delivery_date = models.DateField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f'Order {self.pk}'


class OrderDetail(models.Model):
    material_order = models.ForeignKey(MaterialOrder, on_delete=models.CASCADE)
    material_by_supplier = models.ForeignKey(
        MaterialBySupplier, on_delete=models.PROTECT)
    quantity = models.IntegerField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f'{self.material_by_supplier.raw_material.inventory_item.name} by {self.material_by_supplier.supplier.name}'
