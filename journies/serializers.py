from rest_framework import serializers

from journies.models import Journey, Crew


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
