from typing import Type

from rest_framework import viewsets, permissions
from rest_framework.serializers import Serializer

from journies.models import Crew, Journey
from journies.serializers import (
    CrewSerializer,
    JourneySerializer,
    JourneyDetailSerializer,
)


class CrewView(viewsets.ModelViewSet):
    queryset = Crew.objects.all()
    serializer_class = CrewSerializer
    permission_classes = (permissions.IsAdminUser,)


class JourneyView(viewsets.ModelViewSet):
    queryset = Journey.objects.all()
    serializer_class = JourneySerializer
    permission_classes = (permissions.IsAdminUser,)

    def get_serializer_class(self) -> Type[Serializer]:
        if self.action == "retrieve":
            return JourneyDetailSerializer
        return JourneySerializer
