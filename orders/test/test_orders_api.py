from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APIClient
import json
from journies.test.test_journeys_api import create_journey
from orders.models import Order

ORDER_URL = reverse("orders:order-list")


class NotAuthenticateOrderTestCase(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.user = get_user_model().objects.create_user(
            email="user@user.com", password="testpass"
        )

    def test_unauthorized_view(self):
        res = self.client.get(ORDER_URL)
        self.assertEqual(res.status_code, status.HTTP_401_UNAUTHORIZED)


class AuthenticateOrderTestCase(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.user = get_user_model().objects.create_user(
            email="user@user.com", password="testpass"
        )
        self.client.force_authenticate(self.user)
        self.order = Order.objects.create(user=self.user)

    def test_order_list(self):
        order_data = {
            "cargo": 1,
            "seat": 2,
            "journey": create_journey().id,
        }
        res = self.client.get(path=ORDER_URL, data=order_data)
        self.assertEqual(res.status_code, status.HTTP_200_OK)

    def test_order_create(self):
        order_data = {
            "tickets": [
                {
                    "cargo": "1",
                    "seat": "2",
                    "journey": f"{create_journey().id}",
                }
            ]
        }

        res = self.client.post(
            path=ORDER_URL,
            data=json.dumps(order_data),
            content_type="application/json",
        )
        self.assertEqual(res.status_code, status.HTTP_201_CREATED)
