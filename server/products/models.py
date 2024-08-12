from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator
import datetime
from inventories.models import InventoryItem
from core.utils import normalize_name, normalize_text


class CarType(models.Model):
    name = models.CharField(max_length=50, unique=True,
                            blank=False, null=False)

    def clean(self):
        self.name = normalize_name(self.name)

    def save(self, *args, **kwargs):
        self.full_clean()
        super(CarType, self).save(*args, **kwargs)

    def __str__(self):
        return self.name


class CarMake(models.Model):
    name = models.CharField(max_length=50, unique=True,
                            blank=False, null=False)

    def clean(self):
        self.name = normalize_name(self.name)

    def save(self, *args, **kwargs):
        self.full_clean()
        super(CarMake, self).save(*args, **kwargs)

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

    def clean(self):
        self.name = normalize_name(self.name)

    def save(self, *args, **kwargs):
        self.full_clean()
        super(CarModel, self).save(*args, **kwargs)

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

    def clean(self):
        self.name = normalize_name(self.name)

    def save(self, *args, **kwargs):
        self.full_clean()
        super(ProductCategory, self).save(*args, **kwargs)

    def __str__(self):
        return self.name


class Product(models.Model):
    image_link = models.URLField(blank=False, null=False)
    price = models.IntegerField(
        blank=False, null=False, validators=[MinValueValidator(0)])
    category = models.ForeignKey(
        ProductCategory, on_delete=models.PROTECT, null=False, blank=False)
    car_model = models.ForeignKey(
        CarModel, on_delete=models.PROTECT, null=False, blank=False)
    inventory_item = models.OneToOneField(
        InventoryItem, on_delete=models.CASCADE, null=False, blank=False)

    def clean(self):
        self.image_link = normalize_text(self.image_link)

    def save(self, *args, **kwargs):
        self.full_clean()
        super(Product, self).save(*args, **kwargs)
