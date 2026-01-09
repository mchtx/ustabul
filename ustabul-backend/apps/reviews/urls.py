from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import ReviewViewSet, ai_chat

router = DefaultRouter()
router.register(r'', ReviewViewSet, basename='review')

urlpatterns = [
    path('', include(router.urls)),
    path('ai/chat/', ai_chat, name='ai-chat'),
]
