from rest_framework import serializers

from routes.models import Station, Route


class CrewSerializer(serializers.ModelSerializer):
    class Meta:
        model = Station
        fields = [
            "id",
            "first_name",
            "last_name",
            "position",
        ]


class JourneySerializer(serializers.ModelSerializer):
    class Meta:
        model = Route
        fields = [
            "id",
            "route",
            "train",
            "crew",
            "departure_time",
        ]
