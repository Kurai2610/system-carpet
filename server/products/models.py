from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator
import datetime
from inventories.models import InventoryItem


class CarType(models.Model):
    name = models.CharField(max_length=50, unique=True,
                            blank=False, null=False)

    def __str__(self):
        return self.name


class CarMake(models.Model):
    name = models.CharField(max_length=50, unique=True,
                            blank=False, null=False)

    def __str__(self):
        return self.name


class CarModel(models.Model):
    name = models.CharField(max_length=50,
                            blank=False, null=False)
    year = models.IntegerField(blank=False, null=False, validators=[
        MinValueValidator(1950), MaxValueValidator(datetime.date.today().year)])
    type = models.ForeignKey(CarType, on_delete=models.PROTECT)
    make = models.ForeignKey(CarMake, on_delete=models.PROTECT)

    class Meta:
        unique_together = ['name', 'year']

    def __str__(self):
        return f'{self.make} {self.name} {self.year}'


class ProductCategory(models.Model):
    name = models.CharField(max_length=50, unique=True,
                            blank=False, null=False)

    def __str__(self):
        return self.name


class Product(models.Model):
    image_link = models.URLField(blank=False, null=False)
    price = models.IntegerField(
        blank=False, null=False, validators=[MinValueValidator(0)])
    category = models.ForeignKey(ProductCategory, on_delete=models.PROTECT)
    car_model = models.ForeignKey(CarModel, on_delete=models.PROTECT)
    inventory_item = models.OneToOneField(
        InventoryItem, on_delete=models.CASCADE, null=False)
