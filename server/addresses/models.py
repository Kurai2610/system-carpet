from django.db import models
from core.utils import normalize_name, normalize_text


class Locality(models.Model):
    name = models.CharField(max_length=50, unique=True, null=False)

    def clean(self):
        normalized_name = normalize_name(self.name)
        self.name = normalized_name

    def save(self, *args, **kwargs):
        self.full_clean()
        super(Locality, self).save(*args, **kwargs)

    def __str__(self) -> str:
        return self.name


class Neighborhood(models.Model):
    name = models.CharField(max_length=50, unique=True, null=False)
    locality = models.ForeignKey("Locality", on_delete=models.PROTECT)

    def clean(self):
        normalized_name = normalize_name(self.name)
        self.name = normalized_name

    def save(self, *args, **kwargs):
        self.full_clean()
        super(Neighborhood, self).save(*args, **kwargs)

    def __str__(self) -> str:
        return self.name


class Address(models.Model):
    details = models.CharField(max_length=60, null=False)
    neighborhood = models.ForeignKey(
        "Neighborhood", on_delete=models.PROTECT)

    def clean(self):
        self.details = normalize_text(self.details)

    def save(self, *args, **kwargs):
        self.full_clean()
        super(Address, self).save(*args, **kwargs)
