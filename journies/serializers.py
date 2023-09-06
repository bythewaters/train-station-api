from rest_framework import serializers

from journies.models import Journey, Crew
from orders.serializer import TicketSeatsSerializer
from routes.serializers import StationSerializer
from trains.serializers import TrainTypeSerializer, TrainSerializer


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
    class Meta:
        model = Journey
        fields = [
            "id",
            "route",
            "train",
            "crew",
            "departure_time",
        ]

    def validate(self, validated_data: dict) -> dict:
        data = super(JourneySerializer, self).validate(validated_data)
        Journey.validate_date(
            validated_data.get("departure_time"),
            serializers.ValidationError,
        )
        return data


class JourneyDetailSerializer(JourneySerializer):
    train_type = TrainTypeSerializer(many=False, read_only=True)
    station = StationSerializer(many=False, read_only=True)
    taken_places = TicketSeatsSerializer(
        source="tickets", many=True, read_only=True
    )

    class Meta:
        model = Journey
        fields = (
            "id",
            "departure_time",
            "arrival_time",
            "route",
            "trip_price",
            "taken_places",
        )
