from django.db import models


class Locality(models.Model):
    name = models.CharField(max_length=50)

    def __str__(self) -> str:
        return self.name


class Neighborhood(models.Model):
    name = models.CharField(max_length=50)
    localities_id = models.ForeignKey("Locality", on_delete=models.CASCADE)

    def __str__(self) -> str:
        return self.name


class Address(models.Model):
    details = models.CharField(max_length=60)
