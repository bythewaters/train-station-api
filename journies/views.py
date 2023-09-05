from rest_framework import viewsets, permissions

from journies.models import Crew, Journey
from journies.serializers import CrewSerializer, JourneySerializer


class CrewView(viewsets.ModelViewSet):
    queryset = Crew.objects.all()
    serializer_class = CrewSerializer
    permission_classes = (permissions.IsAdminUser,)


class JourneyView(viewsets.ModelViewSet):
    queryset = Journey.objects.all()
    serializer_class = JourneySerializer
    permission_classes = (permissions.IsAdminUser,)
