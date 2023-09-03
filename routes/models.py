from django.contrib.gis.db import models as gis_models
from django.db import models


class Station(models.Model):
    name = models.CharField(max_length=255, unique=True)
    coordinate = gis_models.PointField(srid=4326, null=True)

    def __str__(self) -> str:
        return self.name


class Route(models.Model):
    source = models.ForeignKey(
        Station, related_name="route_source", on_delete=models.CASCADE
    )
    destination = models.ForeignKey(
        Station, related_name="route_destination", on_delete=models.CASCADE
    )
    distance = models.IntegerField(null=True)

    def __str__(self) -> str:
        return f"{self.source} - {self.destination}"
