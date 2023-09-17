import copy
from datetime import timedelta
from django.forms.models import model_to_dict
from django.contrib.gis.geos import GEOSGeometry
from django.test import TestCase
from django.contrib.auth import get_user_model
from django.utils import timezone
from rest_framework import status
from rest_framework.test import APIClient
from django.urls import reverse
from journies.models import Crew, Journey, TRIP_PRICE_PER_ONE_KM, TAX
from journies.serializers import CrewSerializer, JourneySerializer
from routes.models import Route, Station
from trains.test.test_trains_api import sample_train

JOURNEYS_URL = reverse("journies:journey-list")
CREW_URL = reverse("journies:crew-list")


def create_crew() -> list[Crew]:
    crew1 = Crew.objects.create(
        first_name="test_name", last_name="test_last", position="test_position"
    )
    crew2 = Crew.objects.create(
        first_name="test_name2",
        last_name="test_last2",
        position="test_position2",
    )
    return [crew1, crew2]


def create_route() -> Route:
    station_a = Station.objects.create(
        name="A", stop_time=10, coordinate=GEOSGeometry("POINT(5 23)")
    )
    station_b = Station.objects.create(
        name="B", stop_time=15, coordinate=GEOSGeometry("POINT(6 24)")
    )
    route = Route.objects.create(source=station_a, destination=station_b)
    return route


def create_journey() -> Journey:
    journey = Journey.objects.create(
        train=sample_train(),
        route=create_route(),
        departure_time=timezone.now() + timedelta(days=1),
    )
    journey.crew.set(create_crew())
    return journey


class NotAuthenticatedUserApiTest(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.user = get_user_model().objects.create_user(
            "test@test.com",
            "testpass",
        )

    def test_read_only_crew_api(self):
        train_res = self.client.get(CREW_URL)
        self.assertEqual(train_res.status_code, status.HTTP_200_OK)

    def test_read_only_journey_api(self):
        train_res = self.client.get(JOURNEYS_URL)
        self.assertEqual(train_res.status_code, status.HTTP_200_OK)


class AuthenticatedUserApiTest(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.user = get_user_model().objects.create_user(
            "test@test3.com",
            "testpass",
        )
        self.client.force_authenticate(self.user)

    def test_access_use_api(self):
        train_res = self.client.get(CREW_URL)
        train_type_res = self.client.get(JOURNEYS_URL)
        self.assertEqual(train_res.status_code, status.HTTP_200_OK)
        self.assertEqual(train_type_res.status_code, status.HTTP_200_OK)

    def test_list_crew(self):
        create_crew()
        res = self.client.get(CREW_URL)
        crew = Crew.objects.order_by("id")
        serializer = CrewSerializer(crew, many=True)

        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(res.data, serializer.data)

    def test_forbidden_create_crew(self):
        defaults = model_to_dict(create_crew()[0])
        res = self.client.post(path=CREW_URL, data=defaults)
        self.assertEqual(res.status_code, status.HTTP_403_FORBIDDEN)

    def test_forbidden_delete_crew(self):
        crew = create_crew()
        res = self.client.delete(path=CREW_URL + f"{crew[0].id}/")
        self.assertEqual(res.status_code, status.HTTP_403_FORBIDDEN)

    def test_list_journey(self):
        create_journey()
        res = self.client.get(JOURNEYS_URL)
        journey = Journey.objects.order_by("id")
        serializer = JourneySerializer(journey, many=True)
        res_data_copy = copy.deepcopy(res.data)
        serializer_data_copy = copy.deepcopy(serializer.data)
        for data in res_data_copy:
            data.pop("tickets_available", None)
        for data in serializer_data_copy:
            data.pop("tickets_available", None)
        self.assertEqual(res_data_copy, serializer_data_copy)
        self.assertEqual(res.status_code, status.HTTP_200_OK)

    def test_forbidden_create_journey(self):
        defaults = model_to_dict(create_journey())
        res = self.client.post(path=CREW_URL, data=defaults)
        self.assertEqual(res.status_code, status.HTTP_403_FORBIDDEN)

    def test_forbidden_delete_journey(self):
        journey = create_journey()
        res = self.client.delete(path=CREW_URL + f"{journey.id}/")
        self.assertEqual(res.status_code, status.HTTP_403_FORBIDDEN)


class AdminUserApiTest(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.admin = get_user_model().objects.create_superuser(
            "test@test3.com",
            "testpass",
        )
        self.client.force_authenticate(self.admin)

    def test_access_use_api(self):
        train_res = self.client.get(CREW_URL)
        train_type_res = self.client.get(JOURNEYS_URL)
        self.assertEqual(train_res.status_code, status.HTTP_200_OK)
        self.assertEqual(train_type_res.status_code, status.HTTP_200_OK)

    def test_access_list_crew(self):
        create_crew()
        res = self.client.get(CREW_URL)
        crew = Crew.objects.order_by("id")
        serializer = CrewSerializer(crew, many=True)

        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(res.data, serializer.data)

    def test_access_create_crew(self):
        defaults = model_to_dict(create_crew()[0])
        res = self.client.post(path=CREW_URL, data=defaults)
        self.assertEqual(res.status_code, status.HTTP_201_CREATED)

    def test_access_delete_crew(self):
        crew = create_crew()
        res = self.client.delete(path=CREW_URL + f"{crew[0].id}/")
        self.assertEqual(res.status_code, status.HTTP_204_NO_CONTENT)

    def test_access_list_journey(self):
        create_journey()
        res = self.client.get(JOURNEYS_URL)
        journey = Journey.objects.order_by("id")
        serializer = JourneySerializer(journey, many=True)
        res_data_copy = copy.deepcopy(res.data)
        serializer_data_copy = copy.deepcopy(serializer.data)

        for data in res_data_copy:
            data.pop("tickets_available", None)

        for data in serializer_data_copy:
            data.pop("tickets_available", None)

        self.assertEqual(res_data_copy, serializer_data_copy)
        self.assertEqual(res.status_code, status.HTTP_200_OK)

    def test_access_create_journey(self):
        journey = create_journey()
        journey_data = model_to_dict(journey)
        journey_data["train"] = journey.train.id
        journey_data["route"] = journey.route.id
        journey_data["crew"] = [c.id for c in journey.crew.all()]
        res = self.client.post(path=JOURNEYS_URL, data=journey_data)
        self.assertEqual(res.status_code, status.HTTP_201_CREATED)

    def test_access_delete_journey(self):
        journey = create_journey()
        res = self.client.delete(path=JOURNEYS_URL + f"{journey.id}/")
        self.assertEqual(res.status_code, status.HTTP_204_NO_CONTENT)

    def test_calculate_distance(self):
        journey = create_journey()
        source = journey.route.source
        stop_station = journey.route.stop_station
        destination = journey.route.destination

        next_station = source
        curr_distance = 0
        for stop_station in stop_station.all():
            curr_distance += next_station.coordinate.distance(
                stop_station.coordinate
            )
            next_station = stop_station
        curr_distance += next_station.coordinate.distance(
            destination.coordinate
        )

        self.assertEqual(curr_distance * 100, journey.distance)

    def test_calculate_journey_price(self):
        journey = create_journey()
        price_services = len(journey.train.train_type.services.all()) * 0.2
        price_without_tax = (
            journey.distance * TRIP_PRICE_PER_ONE_KM + price_services
        )
        curr_price = round(price_without_tax + price_without_tax * TAX, 2)

        self.assertEqual(curr_price, journey.trip_price)

    def test_calculate_arrival_time(self):
        journey = create_journey()
        duration = journey.distance / (
            journey.train.train_type.max_speed // 1.5
        )
        if journey.route.stop_station:
            for station in journey.route.stop_station.all():
                duration += station.stop_time / 60
        journey_duration = timedelta(hours=duration)
        arrival_time = journey.departure_time + journey_duration

        self.assertEqual(arrival_time, journey.arrival_time)
