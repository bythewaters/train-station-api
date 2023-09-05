from datetime import timedelta, datetime
from typing import Type

from django.db import models
from django.utils import timezone
from rest_framework.exceptions import ValidationError

from routes.models import Route
from trains.models import Train


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

    def calculate_arrival_time(self) -> datetime:
        """
        Auto calculate approximately arrival time train
        :return:
        arrival_time type datetime
        """
        duration = self.route.distance / (
            self.train.train_type.max_speed // 1.5
        )
        if self.route.stop_station:
            for station in self.route.stop_station.all():
                duration += station.stop_time / 60
        journey_duration = timedelta(hours=duration)
        arrival_time = self.departure_time + journey_duration
        return arrival_time

    def save(self, *args, **kwargs):
        self.clean()
        if self.route and self.train and self.departure_time:
            self.arrival_time = self.calculate_arrival_time()
        super().save(*args, **kwargs)

    @staticmethod
    def validate_date(
        departure_time: datetime,
        error_to_raise: Type[ValidationError],
    ):
        if departure_time < timezone.now():
            raise error_to_raise("Departure time must be in the future.")

    def clean(self) -> None:
        super().clean()
        if self.departure_time <= timezone.now():
            raise ValidationError("Departure time must be in the future.")

    def __str__(self) -> str:
        return (f"{self.route.source.name} - "
                f"{self.route.destination.name}")
