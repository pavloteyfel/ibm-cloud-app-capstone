from django.db import models
from django.db.models.deletion import CASCADE
from django.utils.timezone import now
from dataclasses import dataclass
from datetime import datetime


class CarMake(models.Model):
    name = models.CharField(max_length=120, null=False)
    description = models.TextField(null=False)

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
    year = models.DateField(null=False)
    type = models.CharField(
        max_length=10, choices=CarModelType.choices, default=CarModelType.SEDAN
    )

    def __str__(self):
        return f"{self.car_make.name} {self.name}"


@dataclass
class CarDealer:
    address: str = None
    city: str = None
    full_name: str = None
    id: int = None
    lat: float = None
    long: float = None
    short_name: str = None
    st: str = None
    state: str = None
    zip: str = None


@dataclass
class DearlerReview:
    id: int = None
    car_make: str = None
    car_model: str = None
    car_year: int = None
    dealership: int = None
    name: str = None
    purchase: bool = None
    purchase_date: datetime = None
    review: str = None
