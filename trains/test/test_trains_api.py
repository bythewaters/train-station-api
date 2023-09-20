from typing import Any

from django.test import TestCase

from django.contrib.auth import get_user_model
from rest_framework import status
from rest_framework.test import APIClient
from django.urls import reverse

from trains.models import Service, TrainType, Train
from trains.serializers import (
    ServiceSerializer,
    TrainTypeSerializer,
    TrainSerializer,
)

TRAIN_URL = reverse("trains:train-list")
TRAIN_TYPE_URL = reverse("trains:traintype-list")
SERVICE_URL = reverse("trains:service-list")


def create_services() -> list[Any]:
    service1 = Service.objects.create(name="TestService1")
    service2 = Service.objects.create(name="TestService2")
    return [service1, service2]


def create_train_type() -> TrainType:
    train_type = TrainType.objects.create(name="TrainTypeTest", max_speed=200)
    services = create_services()
    train_type.services.set(services)
    return train_type


def sample_train():
    train = Train.objects.create(
        name="TrainTest",
        cargo_num=10,
        places_in_cargo=30,
        train_type_id=create_train_type().id,
    )
    return train


class NotAdminUserApiTest(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.user = get_user_model().objects.create_user(
            "test@test.com",
            "testpass",
        )
        self.client.force_authenticate(self.user)

    def test_forbidden_use_api(self):
        train_res = self.client.get(TRAIN_URL)
        train_type_res = self.client.get(TRAIN_TYPE_URL)
        services_res = self.client.get(SERVICE_URL)
        self.assertEqual(train_res.status_code, status.HTTP_403_FORBIDDEN)
        self.assertEqual(train_type_res.status_code, status.HTTP_403_FORBIDDEN)
        self.assertEqual(services_res.status_code, status.HTTP_403_FORBIDDEN)


class AdminUserApiTest(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.admin = get_user_model().objects.create_superuser(
            email="admin@admin.com", password="testpass"
        )
        self.client.force_authenticate(self.admin)

    def test_access_use_api(self):
        train_res = self.client.get(TRAIN_URL)
        train_type_res = self.client.get(TRAIN_TYPE_URL)
        services_res = self.client.get(SERVICE_URL)
        self.assertEqual(train_res.status_code, status.HTTP_200_OK)
        self.assertEqual(train_type_res.status_code, status.HTTP_200_OK)
        self.assertEqual(services_res.status_code, status.HTTP_200_OK)

    def test_list_services(self):
        create_services()
        res = self.client.get(SERVICE_URL)
        services = Service.objects.order_by("id")
        serializer = ServiceSerializer(services, many=True)

        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(res.data, serializer.data)

    def test_create_services(self):
        defaults = {"name": "TestService"}
        res = self.client.post(path=SERVICE_URL, data=defaults)
        self.assertEqual(res.status_code, status.HTTP_201_CREATED)

    def test_delete_services(self):
        services = create_services()
        res = self.client.delete(path=SERVICE_URL + f"{services[0].id}/")
        self.assertEqual(res.status_code, status.HTTP_204_NO_CONTENT)

    def test_list_train_type(self):
        create_train_type()
        res = self.client.get(TRAIN_TYPE_URL)
        train_type = TrainType.objects.order_by("id")
        serializer = TrainTypeSerializer(train_type, many=True)

        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(res.data, serializer.data)

    def test_create_train_type(self):
        services = create_services()
        defaults = {
            "name": "TestTrainType",
            "max_speed": 200,
            "services": [service.id for service in services],
        }
        res = self.client.post(path=TRAIN_TYPE_URL, data=defaults)
        self.assertEqual(res.status_code, status.HTTP_201_CREATED)

    def test_delete_train_type(self):
        train_type = create_train_type()
        res = self.client.delete(path=TRAIN_TYPE_URL + f"{train_type.id}/")
        self.assertEqual(res.status_code, status.HTTP_204_NO_CONTENT)

    def test_list_train(self):
        sample_train()
        res = self.client.get(TRAIN_URL)
        train = Train.objects.order_by("id")
        serializer = TrainSerializer(train, many=True)

        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(res.data, serializer.data)

    def test_create_train(self):
        train_type = create_train_type()
        response = self.client.post(
            TRAIN_URL,
            {
                "name": "TestTrain",
                "cargo_num": 3,
                "places_in_cargo": 10,
                "train_type": train_type.id,
            },
        )

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        train = Train.objects.get(name="TestTrain")
        self.assertEqual(train.name, "TestTrain")
        self.assertEqual(train.cargo_num, 3)
        self.assertEqual(train.places_in_cargo, 10)

    def test_delete_train(self):
        train = sample_train()
        res = self.client.delete(path=TRAIN_URL + f"{train.id}/")
        self.assertEqual(res.status_code, status.HTTP_204_NO_CONTENT)
