from rest_framework import serializers

from journies.models import Journey, Crew
from orders.serializer import TicketSeatsSerializer
from routes.serializers import StationSerializer, RouteSerializer
from trains.serializers import TrainSerializer


class CrewSerializer(serializers.ModelSerializer):
    class Meta:
        model = Crew
        fields = [
            "id",
            "first_name",
            "last_name",
            "position",
        ]


class JourneySerializer(serializers.ModelSerializer):
    route = RouteSerializer(many=False, read_only=True)
    tickets_available = serializers.IntegerField(
        read_only=True
    )

    class Meta:
        model = Journey
        fields = [
            "id",
            "route",
            "departure_time",
            "arrival_time",
            "tickets_available",
        ]

    def validate(self, validated_data: dict) -> dict:
        data = super(JourneySerializer, self).validate(validated_data)
        Journey.validate_date(
            validated_data.get("departure_time"),
            serializers.ValidationError,
        )
        return data


class JourneyDetailSerializer(JourneySerializer):
    train = TrainSerializer(many=False, read_only=True)
    station = StationSerializer(many=False, read_only=True)
    route = RouteSerializer(many=False, read_only=True)
    taken_seats = TicketSeatsSerializer(
        source="ticket", many=True, read_only=True
    )

    class Meta:
        model = Journey
        fields = (
            "id",
            "departure_time",
            "arrival_time",
            "route",
            "distance",
            "station",
            "train",
            "taken_seats",
        )


class JourneyCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Journey
        fields = [
            "id",
            "route",
            "train",
            "crew",
            "departure_time",
        ]
