from django.db import models
from django.core.validators import MinValueValidator


class Status(models.Model):
    name = models.CharField(max_length=100, unique=True, null=False)

    def __str__(self):
        return self.name


class Type(models.Model):
    name = models.CharField(max_length=100, unique=True, null=False)
    low_stock_threshold = models.IntegerField(
        default=10, null=False, validators=[MinValueValidator(0)]
    )
    out_of_stock_threshold = models.IntegerField(
        default=0, null=False, validators=[MinValueValidator(0)])

    def __str__(self):
        return self.name


class InventoryItem(models.Model):
    name = models.CharField(max_length=100, unique=True, null=False)
    description = models.TextField(default='', null=True, blank=True)
    stock = models.IntegerField(null=False, validators=[MinValueValidator(0)])
    status = models.ForeignKey(Status, on_delete=models.PROTECT)
    type = models.ForeignKey(Type, on_delete=models.PROTECT)

    def save(self, *args, **kwargs):
        if self.stock <= self.type.out_of_stock_threshold:
            self.status = Status.objects.get(name='Out of Stock')
        elif self.stock <= self.type.low_stock_threshold:
            self.status = Status.objects.get(name='Low Stock')
        else:
            self.status = Status.objects.get(name='Available')
        super().save(*args, **kwargs)

    def __str__(self):
        return self.name
