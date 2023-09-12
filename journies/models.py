from datetime import timedelta, datetime
from typing import Type

from django.db import models
from django.utils import timezone
from django.core.validators import ValidationError

from routes.models import Route
from trains.models import Train

TRIP_PRICE_PER_ONE_KM = 0.10
TAX = 0.2


class Crew(models.Model):
    first_name = models.CharField(max_length=255)
    last_name = models.CharField(max_length=255)
    position = models.CharField(max_length=255)

    def __str__(self) -> str:
        return f"{self.first_name} {self.last_name}"


class Journey(models.Model):
    route = models.ForeignKey(
        Route, on_delete=models.CASCADE, related_name="journey"
    )
    train = models.ForeignKey(
        Train, on_delete=models.CASCADE, related_name="journey"
    )
    crew = models.ManyToManyField(Crew, related_name="journey")
    departure_time = models.DateTimeField()
    arrival_time = models.DateTimeField(blank=True, null=True)
    trip_price = models.FloatField(blank=True, null=True)
    distance = models.IntegerField(null=True, blank=True)

    def calculate_distance(self) -> int:
        """
        Calculate distance between 2 stations
        :return:
        distance type int
        """
        next_station = self.route.source
        distance = 0
        for stop_station in self.route.stop_station.all():
            distance += next_station.coordinate.distance(stop_station.coordinate)
            next_station = stop_station
        distance += next_station.coordinate.distance(self.route.destination.coordinate)
        return distance * 100

    def calculate_trip_price(self) -> float:
        """
        Auto calculate journey price
        :return:
        trip_price type float
        """
        price_services = len(self.train.train_type.services.all()) * 0.2
        price_without_tax = (
            self.distance * TRIP_PRICE_PER_ONE_KM + price_services
        )
        return price_without_tax + price_without_tax * TAX

    def calculate_arrival_time(self) -> datetime:
        """
        Auto calculate approximately arrival time train
        :return:
        arrival_time type datetime
        """
        duration = self.distance / (
            self.train.train_type.max_speed // 1.5
        )
        if self.route.stop_station:
            for station in self.route.stop_station.all():
                duration += station.stop_time / 60
        journey_duration = timedelta(hours=duration)
        arrival_time = self.departure_time + journey_duration
        return arrival_time

    @staticmethod
    def validate_date(
        departure_time: datetime,
        error_to_raise: Type[ValidationError],
    ) -> None:
        if departure_time < timezone.now():
            raise error_to_raise("Departure time must be in the future.")

    def clean(self) -> None:
        super().clean()
        if self.departure_time <= timezone.now():
            raise ValidationError("Departure time must be in the future.")

    def save(self, *args, **kwargs) -> None:
        self.clean()
        if self.route.source and self.route.destination:
            self.distance = self.calculate_distance()
        if self.route and self.train and self.departure_time:
            self.arrival_time = self.calculate_arrival_time()
        if not self.trip_price:
            self.trip_price = round(self.calculate_trip_price())
        super().save(*args, **kwargs)

    def __str__(self) -> str:
        return (f"{self.route.source.name} - "
                f"{self.route.destination.name}")
