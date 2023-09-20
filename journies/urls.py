from django.urls import path, include
from rest_framework import routers

from journies.views import JourneyView, CrewView


router = routers.DefaultRouter()
router.register("all", JourneyView)
router.register("crew", CrewView)

urlpatterns = [path("", include(router.urls))]

app_name = "journies"
