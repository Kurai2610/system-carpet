from django.db import models, IntegrityError
from django.core.exceptions import ValidationError
from core.utils import normalize_name


class Locality(models.Model):
    name = models.CharField(max_length=50, unique=True, null=False)

    def clean(self):
        normalized_name = normalize_name(self.name)
        if Locality.objects.filter(name=normalized_name).exists():
            raise ValidationError(
                'A locality with this name already exists.',
                code='duplicate_name',
                params={'name': normalized_name}
            )
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
        if Neighborhood.objects.filter(name=normalized_name).exists():
            raise ValidationError(
                'A neighborhood with this name already exists.',
                code='duplicate_name',
                params={'name': normalized_name}
            )
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
