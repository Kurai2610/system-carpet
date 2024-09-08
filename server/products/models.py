import datetime
from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator
from inventories.models import InventoryItem
from .validators import validate_material_is_raw


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
    discount = models.IntegerField(
        validators=[
            MinValueValidator(0),
            MaxValueValidator(100)
        ],
        default=0
    )

    def __str__(self):
        return self.name


class CustomOption(models.Model):
    name = models.CharField(max_length=50, blank=False,
                            null=False, unique=True)
    required = models.BooleanField(default=False)
    description = models.TextField(blank=True, null=True)


class CustomOptionDetail(models.Model):
    custom_option = models.ForeignKey(
        CustomOption, on_delete=models.CASCADE, null=False, blank=False)
    name = models.CharField(max_length=50, blank=False,
                            null=False, unique=True)
    image_url = models.URLField(blank=False, null=False)
    price = models.IntegerField(
        blank=False, null=False, validators=[MinValueValidator(0)])


class Carpet(models.Model):
    image_link = models.URLField(blank=False, null=False)
    price = models.IntegerField(
        blank=False, null=False, validators=[MinValueValidator(0)])
    category = models.ForeignKey(
        ProductCategory, on_delete=models.PROTECT, null=False, blank=False)
    car_model = models.ForeignKey(
        CarModel, on_delete=models.PROTECT, null=False, blank=False)
    inventory_item = models.OneToOneField(
        InventoryItem, on_delete=models.CASCADE, null=False, blank=False)
    material = models.ForeignKey(
        InventoryItem, on_delete=models.PROTECT, related_name='material', null=False, blank=False, validators=[validate_material_is_raw])
    custom_options = models.ManyToManyField(
        CustomOption, blank=True, null=True)
