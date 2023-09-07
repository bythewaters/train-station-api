from django.contrib.gis.geos import Point
from rest_framework import serializers

from routes.models import Station, Route


class StationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Station
        fields = [
            "id",
            "name",
            "coordinate",
        ]

    def get_coordinate(self, obj) -> Point | None:
        """
        Get the Point geometry based on the provided coordinates,
        and format request coordinate data in Point instance for create
        new place.

        Args:
            obj: The object for which to get the Point geometry.
        Returns:
            Point | None: The Point geometry if coordinates are provided, otherwise None.
        Raises:
            serializers.ValidationError: If the coordinates are not in the correct format.
        """

        coordinates = self.context["request"].data.get("coordinate")
        if coordinates:
            try:
                lon, lat = map(float, coordinates.split(","))
            except ValueError:
                raise serializers.ValidationError(
                    "You must set coordinate in format: 'number, number'"
                )
            return Point(lon, lat)
        return None


class StationNameSerializer(StationSerializer):
    class Meta:
        model = Station
        fields = [
            "id",
            "name",
        ]


class RouteSerializer(serializers.ModelSerializer):
    source_info = serializers.CharField(source="source.name", read_only=True)
    destination_info = serializers.CharField(source="destination.name", read_only=True)

    class Meta:
        model = Route
        fields = [
            "id",
            "source_info",
            "destination_info",
            "distance",
        ]
