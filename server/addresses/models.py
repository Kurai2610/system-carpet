from django.db import models
from django.core.exceptions import ValidationError


class Locality(models.Model):
    name = models.CharField(max_length=50, unique=True, null=False)

    def clean(self):
        normalized_name = self.name.lower()
        if Locality.objects.filter(name=normalized_name).exists():
            raise ValidationError()

    def save(self, *args, **kwargs):
        self.name = self.name.capitalize()
        self.full_clean()
        super(Locality, self).save(*args, **kwargs)

    def __str__(self) -> str:
        return self.name


class Neighborhood(models.Model):
    name = models.CharField(max_length=50, unique=True, null=False)
    locality = models.ForeignKey("Locality", on_delete=models.PROTECT)

    def clean(self):
        normalized_name = self.name.lower()
        if Neighborhood.objects.filter(name=normalized_name).exists():
            raise ValidationError()

    def save(self, *args, **kwargs):
        self.name = self.name.capitalize()
        self.full_clean()
        super(Neighborhood, self).save(*args, **kwargs)

    def __str__(self) -> str:
        return self.name


class Address(models.Model):
    details = models.CharField(max_length=60, null=False)
    neighborhood = models.ForeignKey(
        "Neighborhood", on_delete=models.PROTECT)
