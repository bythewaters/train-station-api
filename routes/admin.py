from django.contrib import admin
from django.contrib.admin import ModelAdmin
from django.contrib.gis.admin import GISModelAdmin

from routes.models import Station, Route


@admin.register(Station)
class TrainAdmin(GISModelAdmin):
    list_display = (
        "name",
        "coordinate",
    )
    ordering = ("name",)
    gis_widget_kwargs = {
        "attrs": {
            "default_zoom": 13,
            "default_lat": 48.97458932856062,
            "default_lon": 14.480637200003383,
        },
    }


@admin.register(Route)
class RouteAdmin(ModelAdmin):
    list_display = (
        "source",
        "destination",
        "stop_stations_names",
    )
    filter_horizontal = ("stop_station",)

    def stop_stations_names(self, obj: Route) -> str:
        return ", ".join(
            [str(station) for station in obj.stop_station.all()]
        )

    stop_stations_names.short_description = "Stop stations"
