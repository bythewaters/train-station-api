from django.contrib import admin
from django.contrib.admin import ModelAdmin

from routes.models import Station, Route


@admin.register(Station)
class TrainAdmin(ModelAdmin):
    list_display = (
        "name",
    )
    ordering = ("name",)


@admin.register(Route)
class TrainAdmin(ModelAdmin):
    list_display = (
        "source",
        "destination",
        "distance",
    )
    ordering = ("distance",)
