from typing import Type

from django.db.models import Count, QuerySet, F
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
    permission_classes = (permissions.IsAuthenticated,)


class JourneyView(viewsets.ModelViewSet):
    queryset = (
        Journey.objects.all()
        .select_related("route__source", "route__destination", "train")
        .prefetch_related("crew__journey")
    )
    serializer_class = JourneySerializer
    permission_classes = (permissions.IsAuthenticated,)

    def get_queryset(self) -> QuerySet:
        queryset = self.queryset
        if self.action == "list":
            queryset = queryset.select_related("train").annotate(
                tickets_available=F("train__places_in_cargo") - Count("ticket")
            )
        return queryset

    def get_serializer_class(self) -> Type[Serializer]:
        if self.action == "retrieve":
            return JourneyDetailSerializer
        return JourneySerializer
