from django.urls import path, include
from rest_framework import routers

from trains.views import TrainTypeViewSet, TrainViewSet, ServiceViewSet

router = routers.DefaultRouter()
router.register("train", TrainViewSet)
router.register("train-type", TrainTypeViewSet)
router.register("service", ServiceViewSet)

urlpatterns = [path("", include(router.urls))]

app_name = "trains"
