from django.urls import path, include
from rest_framework.routers import DefaultRouter

from .views import MapViewSet, update_routes_data

router = DefaultRouter()
router.register(r'', MapViewSet, basename='route-planner')


urlpatterns = [
    path('', include(router.urls)),
    path('update-routes', update_routes_data) 
]
