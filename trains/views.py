from rest_framework import viewsets, permissions

from trains.models import TrainType, Train
from trains.serializers import TrainTypeSerializer, TrainSerializer


class TrainTypeViewSet(viewsets.ModelViewSet):
    queryset = TrainType.objects.all()
    serializer_class = TrainTypeSerializer
    permission_classes = (permissions.IsAdminUser,)


class TrainViewSet(viewsets.ModelViewSet):
    queryset = Train.objects.all()
    serializer_class = TrainSerializer
    permission_classes = (permissions.IsAdminUser,)
