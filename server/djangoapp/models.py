from django.db import models
from django.db.models.deletion import CASCADE
from django.utils.timezone import now
from dataclasses import dataclass
from datetime import datetime


class CarMake(models.Model):
    name = models.CharField(max_length=120, null=False)
    description = models.TextField()

    def __str__(self):
        return f"{self.name}"


class CarModel(models.Model):
    class CarModelType(models.TextChoices):
        SUV = "SUV"
        WAGON = "Wagon"
        SEDAN = "Sedan"
        COUPE = "Coupe"
        MINIVAN = "Minivan"

    car_make = models.ForeignKey(CarMake, on_delete=models.CASCADE)
    name = models.CharField(max_length=120, null=False)
    dealerid = models.IntegerField(null=False)
    year = models.IntegerField(null=False)
    type = models.CharField(
        max_length=10, choices=CarModelType.choices, default=CarModelType.SEDAN
    )

    def __str__(self):
        return f"{self.car_make.name} {self.name}"
