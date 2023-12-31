from rest_framework import viewsets, permissions

from trains.models import TrainType, Train, Service
from trains.serializers import (
    TrainTypeSerializer,
    TrainSerializer,
    ServiceSerializer,
)


class TrainTypeViewSet(viewsets.ModelViewSet):
    queryset = TrainType.objects.all().prefetch_related("services__train_type")
    serializer_class = TrainTypeSerializer
    permission_classes = (permissions.IsAdminUser,)


class TrainViewSet(viewsets.ModelViewSet):
    queryset = Train.objects.all().select_related("train_type")
    serializer_class = TrainSerializer
    permission_classes = (permissions.IsAdminUser,)


class ServiceViewSet(viewsets.ModelViewSet):
    queryset = Service.objects.all()
    serializer_class = ServiceSerializer
    permission_classes = (permissions.IsAdminUser,)
