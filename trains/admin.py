from django.contrib import admin
from django.contrib.admin import ModelAdmin

from trains.models import TrainType, Train


@admin.register(TrainType)
class TrainTypeAdmin(ModelAdmin):
    list_display = (
        "name",
        "services"
    )
    ordering = ("name",)
    list_filter = ("services",)


@admin.register(Train)
class TrainAdmin(ModelAdmin):
    list_display = (
        "name",
        "cargo_num",
        "places_in_cargo",
        "train_type",
    )
    ordering = ("name",)
    list_filter = ("train_type",)
