from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import (
    CategoryViewSet, WorkshopViewSet, WorkingHoursViewSet, ServiceViewSet
)

router = DefaultRouter()
router.register(r'categories', CategoryViewSet, basename='category')
router.register(r'', WorkshopViewSet, basename='workshop')
router.register(r'working-hours', WorkingHoursViewSet, basename='working-hours')
router.register(r'services', ServiceViewSet, basename='service')

urlpatterns = [
    path('', include(router.urls)),
]
