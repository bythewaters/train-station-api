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

# TODO I must add feature it calculate distance between 2 stations
@admin.register(Route)
class TrainAdmin(ModelAdmin):
    list_display = (
        "source",
        "destination",
        "distance",
    )
    ordering = ("distance",)
