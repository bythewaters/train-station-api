from django.contrib import admin
from django.contrib.admin import ModelAdmin

from journies.models import Crew, Journey


@admin.register(Crew)
class CrewAdmin(ModelAdmin):
    list_display = (
        "first_name",
        "last_name",
        "position",
    )
    ordering = ("position",)


@admin.register(Journey)
class JourneyAdmin(ModelAdmin):
    list_display = (
        "route",
        "train",
        "departure_time",
        "arrival_time",
        "distance",
        "crew_names",
    )
    ordering = ("train", "departure_time", "arrival_time")
    filter_horizontal = ("crew",)

    def crew_names(self, obj: Journey) -> str:
        return ", ".join([str(crew) for crew in obj.crew.all()])

    crew_names.short_description = "Crew"
