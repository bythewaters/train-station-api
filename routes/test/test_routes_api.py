from django.contrib.auth import get_user_model
from django.contrib.gis.geos import GEOSGeometry
from django.test import TestCase
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase, APIClient
from routes.models import Station, Route


class StationTestCase(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.admin = get_user_model().objects.create_superuser(
            email="admin@admin.com", password="testpass"
        )
        self.client.force_authenticate(self.admin)

    def test_create_station(self):
        url = reverse("routes:station-list")
        data = {"name": "C", "stop_time": 15, "coordinate": "POINT(7 25)"}
        response = self.client.post(url, data, format="json")

        # Check status and count after creation
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Station.objects.count(), 1)

    def test_delete_station(self):
        station_c = Station.objects.create(
            name="C", stop_time=15, coordinate=GEOSGeometry("POINT(7 25)")
        )
        url = reverse("routes:station-detail", kwargs={"pk": station_c.pk})
        response = self.client.delete(url)

        # Check status and count after deletion
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(Station.objects.count(), 0)


class RouteTestCase(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.admin = get_user_model().objects.create_superuser(
            email="admin@admin.com", password="testpass"
        )
        self.client.force_authenticate(self.admin)
        self.station_a = Station.objects.create(
            name="A", stop_time=10, coordinate=GEOSGeometry("POINT(5 23)")
        )
        self.station_b = Station.objects.create(
            name="B", stop_time=15, coordinate=GEOSGeometry("POINT(6 24)")
        )
        self.route = Route.objects.create(
            source=self.station_a, destination=self.station_b
        )

    def test_route_created(self):
        self.assertIsInstance(self.route, Route)
        self.assertEqual(self.route.source.name, "A")
        self.assertEqual(self.route.destination.name, "B")

    def test_delete_route(self):
        url = reverse("routes:route-detail", kwargs={"pk": self.route.pk})
        response = self.client.delete(url)

        # Check status and count after deletion
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(Route.objects.count(), 0)


class StationListViewTest(APITestCase):
    def setUp(self):
        self.client = APIClient()
        self.admin = get_user_model().objects.create_superuser(
            email="admin@admin.com", password="testpass"
        )
        self.client.force_authenticate(self.admin)
        self.station_a = Station.objects.create(
            name="A", stop_time=10, coordinate=GEOSGeometry("POINT(5 23)")
        )
        self.station_b = Station.objects.create(
            name="B", stop_time=20, coordinate=GEOSGeometry("POINT(6 24)")
        )

    def test_station_list_view(self):
        url = reverse("routes:station-list")

        # Get method test
        response = self.client.get(url, format="json")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 2)  # We have 2 stations


class RouteViewTest(APITestCase):
    def setUp(self):
        self.client = APIClient()
        self.admin = get_user_model().objects.create_superuser(
            email="admin@admin.com", password="testpass"
        )
        self.client.force_authenticate(self.admin)
        self.station_a = Station.objects.create(
            name="A", stop_time=10, coordinate=GEOSGeometry("POINT(5 23)")
        )
        self.station_b = Station.objects.create(
            name="B", stop_time=20, coordinate=GEOSGeometry("POINT(6 24)")
        )
        self.route = Route.objects.create(
            source=self.station_a, destination=self.station_b
        )

    def test_route_view(self):
        url = reverse("routes:route-list")

        # Get method test
        response = self.client.get(url, format="json")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)  # We have 1 route created
