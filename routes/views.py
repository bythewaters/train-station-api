from django.contrib.gis.geos import Point
from django.contrib.gis.db.models.functions import Distance as DistanceFunc
from django.db.models import QuerySet
from drf_spectacular.types import OpenApiTypes
from drf_spectacular.utils import extend_schema, OpenApiParameter
from geopy.geocoders import Nominatim
from rest_framework import viewsets, permissions
from rest_framework.exceptions import ValidationError
from rest_framework.request import Request

from routes.models import Station, Route
from routes.serializers import StationSerializer, RouteSerializer

geolocator = Nominatim(user_agent="station")


class StationListView(viewsets.ModelViewSet):
    serializer_class = StationSerializer
    queryset = Station.objects.all()
    permission_classes = (permissions.IsAdminUser,)

    def get_queryset(self) -> QuerySet[Station]:
        """
        Get the queryset of stations with optional coordinate parameter
        Args:
            self: The instance of the view.
        Returns:
            QuerySet[Station]: The filtered queryset of stations.
        Raises:
            ValidationError: If the coordinate is not provided in the correct format.
        """
        queryset = self.queryset
        coordinate = self.request.query_params.get("coordinate", None)
        if coordinate:
            try:
                lon, lat = map(float, coordinate.split(","))
                point = Point(float(lon), float(lat), srid=4326)
            except ValueError:
                raise ValidationError("You must set geom in format: 'number,number'")
            return queryset.annotate(
                distance=DistanceFunc("coordinate", point)
            ).order_by(
                "distance"
            )[:1]
        return queryset

    def perform_create(self, serializer: StationSerializer) -> None:
        address = serializer.initial_data["coordinate"]
        geo_coordinate = geolocator.geocode(address)
        if geo_coordinate is not None:
            lat = geo_coordinate.latitude
            lng = geo_coordinate.longitude
            point = Point(lng, lat)
            serializer.save(coordinate=point)

    @extend_schema(
        parameters=[
            OpenApiParameter(
                "coordinate",
                type=OpenApiTypes.STR,
                description="finding the nearest station to "
                            "the entered coordinates "
                            "ex.(?coordinate=56.3443,30.4343)",
            )]
    )
    def list(self, request: Request, *args, **kwargs) -> list:
        return super().list(request, *args, **kwargs)


class RouteView(viewsets.ModelViewSet):
    queryset = Route.objects.all()
    serializer_class = RouteSerializer
    permission_classes = (permissions.IsAdminUser,)
