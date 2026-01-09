from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.filters import SearchFilter, OrderingFilter
from .models import Category, Workshop, WorkingHours, Service
from .serializers import (
    CategorySerializer, WorkshopListSerializer, WorkshopDetailSerializer,
    WorkingHoursSerializer, ServiceSerializer
)


class CategoryViewSet(viewsets.ReadOnlyModelViewSet):
    """Kategori listeleme"""
    queryset = Category.objects.all()
    serializer_class = CategorySerializer


class WorkshopViewSet(viewsets.ModelViewSet):
    """Dükkân yönetimi"""
    queryset = Workshop.objects.filter(is_active=True)
    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    filterset_fields = ['category', 'district', 'is_premium', 'is_closed_today']
    search_fields = ['name', 'description', 'address']
    ordering_fields = ['average_rating', 'total_reviews', 'created_at']
    
    def get_serializer_class(self):
        if self.action == 'retrieve':
            return WorkshopDetailSerializer
        return WorkshopListSerializer
    
    def get_queryset(self):
        queryset = super().get_queryset()
        
        # Puan filtreleme
        min_rating = self.request.query_params.get('min_rating')
        if min_rating:
            queryset = queryset.filter(average_rating__gte=float(min_rating))
        
        return queryset
    
    @action(detail=False, methods=['get'])
    def my_workshops(self, request):
        """Kullanıcının dükkanları"""
        if not request.user.is_authenticated:
            return Response({'detail': 'Kimlik doğrulaması gerekli.'}, status=status.HTTP_401_UNAUTHORIZED)
        
        workshops = Workshop.objects.filter(owner=request.user)
        serializer = WorkshopDetailSerializer(workshops, many=True)
        return Response(serializer.data)


class WorkingHoursViewSet(viewsets.ModelViewSet):
    """Çalışma saatleri yönetimi"""
    queryset = WorkingHours.objects.all()
    serializer_class = WorkingHoursSerializer


class ServiceViewSet(viewsets.ModelViewSet):
    """Hizmet yönetimi"""
    queryset = Service.objects.all()
    serializer_class = ServiceSerializer
