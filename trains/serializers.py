from rest_framework import serializers

from trains.models import TrainType, Train, Service


class ServiceSerializer(serializers.ModelSerializer):
    class Meta:
        model = Service
        fields = [
            "name",
        ]


class TrainTypeSerializer(serializers.ModelSerializer):
    services = ServiceSerializer(many=True, read_only=True)

    class Meta:
        model = TrainType
        fields = [
            "id",
            "name",
            "max_speed",
            "services",
        ]


class TrainSerializer(serializers.ModelSerializer):
    train_type = serializers.CharField(
        source="train_type.name", read_only=True
    )

    class Meta:
        model = Train
        fields = [
            "id",
            "name",
            "cargo_num",
            "places_in_cargo",
            "train_type",
        ]
