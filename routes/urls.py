from django.urls import path, include
from rest_framework import routers

from routes.views import RouteView, StationListView

router = routers.DefaultRouter()
router.register("all", RouteView)
router.register("stations", StationListView)

urlpatterns = [path("", include(router.urls))]

app_name = "routes"
