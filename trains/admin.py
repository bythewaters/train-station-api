from django.contrib import admin
from django.contrib.admin import ModelAdmin

from trains.models import TrainType, Train, Service


@admin.register(TrainType)
class TrainTypeAdmin(ModelAdmin):
    list_display = ("name", "service_names",)
    ordering = ("name",)
    filter_horizontal = ("services",)

    def service_names(self, obj):
        return ", ".join(
            [str(p) for p in obj.services.all()]
        )

    service_names.short_description = "Services"


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


admin.site.register(Service)
