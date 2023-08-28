from rest_framework import serializers

from trains.models import TrainType, Train, Service


class TrainTypeSerializer(serializers.ModelSerializer):
    class Meta:
        model = TrainType
        fields = [
            "id",
            "name",
            "services",
        ]


class TrainSerializer(serializers.ModelSerializer):
    class Meta:
        model = Train
        fields = [
            "id",
            "name",
            "cargo_num",
            "places_in_cargo",
            "train_type",
        ]


class ServiceSerializer(serializers.ModelSerializer):
    class Meta:
        model = Service
        fields = [
            "id",
            "name",
        ]
