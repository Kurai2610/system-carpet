from django.db import models
from django.core.validators import MinValueValidator


class InventoryItem(models.Model):
    TYPE_CHOICES = [
        ('MAT', 'Tapete'),
        ('RAW', 'Materia Prima'),
    ]

    name = models.CharField(max_length=100, unique=True, null=False)
    description = models.TextField(default='', null=True, blank=True)
    stock = models.IntegerField(
        null=False, validators=[MinValueValidator(0)])
    type = models.CharField(max_length=3, choices=TYPE_CHOICES, null=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    @property
    def status(self):
        thresholds = {
            'MAT': {'low_stock_threshold': 10, 'out_of_stock_threshold': 0},
            'RAW': {'low_stock_threshold': 40, 'out_of_stock_threshold': 0},
        }

        current_thresholds = thresholds.get(self.type)

        if self.stock <= current_thresholds['out_of_stock_threshold']:
            return 'Out of stock'

        elif current_thresholds['low_stock_threshold'] is not None and self.stock <= current_thresholds['low_stock_threshold']:
            return 'Low stock'
        else:
            return 'Available'

    def __str__(self):
        return self.name
