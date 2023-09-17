from django.contrib.gis.db import models as gis_models
from django.db import models


class Station(models.Model):
    name = models.CharField(max_length=255, unique=True)
    coordinate = gis_models.PointField(srid=4326, null=True)
    stop_time = models.IntegerField(blank=True, null=True)

    def __str__(self) -> str:
        return self.name


class Route(models.Model):
    source = models.ForeignKey(
        Station, related_name="route_source", on_delete=models.CASCADE
    )
    stop_station = models.ManyToManyField(
        Station, related_name="route", blank=True
    )
    destination = models.ForeignKey(
        Station, related_name="route_destination", on_delete=models.CASCADE
    )

    def __str__(self) -> str:
        return f"{self.source.name} - {self.destination.name}"
