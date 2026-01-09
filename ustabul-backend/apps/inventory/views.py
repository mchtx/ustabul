from rest_framework import viewsets, status, filters, serializers
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from django.db.models import Q, F
from django.db import transaction
from apps.users.permissions import IsPremiumPro
from .models import (
    Vehicle, PartCategory, Part, PartCompatibility,
    AlternativePart, PartNote, PurchasePrice,
    SalePrice, StockMovement
)
from .serializers import (
    VehicleSerializer, PartCategorySerializer,
    PartSerializer, PartListSerializer, PartCreateSerializer,
    PartCompatibilitySerializer, AlternativePartSerializer,
    PartNoteSerializer, PurchasePriceSerializer,
    SalePriceSerializer, StockMovementSerializer
)


class VehicleViewSet(viewsets.ModelViewSet):
    """Araç yönetimi"""
    queryset = Vehicle.objects.all()
    serializer_class = VehicleSerializer
    permission_classes = [IsAuthenticated]
    filter_backends = [filters.SearchFilter, filters.OrderingFilter]
    search_fields = ['brand', 'model', 'engine', 'engine_code']
    ordering_fields = ['brand', 'model', 'year_from']
    ordering = ['brand', 'model']


class PartCategoryViewSet(viewsets.ReadOnlyModelViewSet):
    """Parça kategorileri - sadece okuma (ön tanımlı)"""
    queryset = PartCategory.objects.filter(is_active=True)
    serializer_class = PartCategorySerializer
    permission_classes = [IsAuthenticated]
    filter_backends = [filters.SearchFilter]
    search_fields = ['name', 'subcategory']


class PartViewSet(viewsets.ModelViewSet):
    """Parça yönetimi"""
    permission_classes = [IsAuthenticated]
    
    def get_queryset(self):
        if self.request.user.is_authenticated:
            return Part.objects.filter(workshop__owner=self.request.user)
        return Part.objects.none()
    
    def get_serializer_class(self):
        if self.action == 'list':
            return PartListSerializer
        elif self.action == 'create':
            return PartCreateSerializer
        return PartSerializer
    
    def perform_create(self, serializer):
        # Workshop ID'yi request'ten al
        workshop_id = self.request.data.get('workshop_id')
        if not workshop_id:
            # Kullanıcının ilk workshop'unu kullan
            workshop = self.request.user.workshops.first()
            if not workshop:
                # Otomatik olarak minimal bir workshop oluştur
                from apps.workshops.models import Workshop
                workshop = Workshop.objects.create(
                    owner=self.request.user,
                    name=f"{self.request.user.username} - Varsayılan Dükkan",
                    category=None,
                    description='Otomatik oluşturulan varsayılan dükkan',
                    address='Adres belirtilmedi',
                    phone='0000000000',
                    district='Belirtilmedi'
                )
        else:
            from apps.workshops.models import Workshop
            try:
                workshop = Workshop.objects.get(id=workshop_id, owner=self.request.user)
            except Workshop.DoesNotExist:
                raise serializers.ValidationError("Dükkan bulunamadı.")
        
        serializer.save(workshop=workshop)

    def create(self, request, *args, **kwargs):
        """Override create to return detailed validation errors and log them."""
        serializer_class = self.get_serializer_class()
        serializer = serializer_class(data=request.data)
        if not serializer.is_valid():
            # Log errors for easier debugging
            import logging
            logger = logging.getLogger(__name__)
            logger.warning(f'Part create validation errors: {serializer.errors}')
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        try:
            with transaction.atomic():
                self.perform_create(serializer)
        except serializers.ValidationError as e:
            return Response({'detail': str(e)}, status=status.HTTP_400_BAD_REQUEST)

        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)
    
    @action(detail=False, methods=['get'])
    def low_stock(self, request):
        """Düşük stok parçaları"""
        parts = self.get_queryset().filter(quantity__lte=F('min_stock'))
        serializer = self.get_serializer(parts, many=True)
        return Response(serializer.data)
    
    @action(detail=True, methods=['post'])
    def add_vehicle(self, request, pk=None):
        """Parçaya araç ekle"""
        part = self.get_object()
        vehicle_id = request.data.get('vehicle_id')
        
        if not vehicle_id:
            return Response(
                {'error': 'vehicle_id gerekli'},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        try:
            vehicle = Vehicle.objects.get(id=vehicle_id)
            compatibility, created = PartCompatibility.objects.get_or_create(
                part=part,
                vehicle=vehicle
            )
            if created:
                return Response({'message': 'Araç eklendi'}, status=status.HTTP_201_CREATED)
            return Response({'message': 'Araç zaten ekli'}, status=status.HTTP_200_OK)
        except Vehicle.DoesNotExist:
            return Response(
                {'error': 'Araç bulunamadı'},
                status=status.HTTP_404_NOT_FOUND
            )
    
    @action(detail=True, methods=['post'])
    def add_alternative(self, request, pk=None):
        """Parçaya alternatif ekle"""
        part = self.get_object()
        alternative_id = request.data.get('alternative_id')
        note = request.data.get('note', '')
        
        if not alternative_id:
            return Response(
                {'error': 'alternative_id gerekli'},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        try:
            alternative = Part.objects.get(id=alternative_id, workshop=part.workshop)
            if alternative.id == part.id:
                return Response(
                    {'error': 'Parça kendisinin alternatifi olamaz'},
                    status=status.HTTP_400_BAD_REQUEST
                )
            
            alt, created = AlternativePart.objects.get_or_create(
                part=part,
                alternative=alternative,
                defaults={'note': note}
            )
            if created:
                return Response({'message': 'Alternatif eklendi'}, status=status.HTTP_201_CREATED)
            return Response({'message': 'Alternatif zaten ekli'}, status=status.HTTP_200_OK)
        except Part.DoesNotExist:
            return Response(
                {'error': 'Alternatif parça bulunamadı'},
                status=status.HTTP_404_NOT_FOUND
            )
    
    @action(detail=True, methods=['post'])
    def add_note(self, request, pk=None):
        """Parçaya not ekle"""
        part = self.get_object()
        note_text = request.data.get('note')
        
        if not note_text:
            return Response(
                {'error': 'note gerekli'},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        note = PartNote.objects.create(
            part=part,
            note=note_text,
            created_by=request.user
        )
        serializer = PartNoteSerializer(note)
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    
    @action(detail=True, methods=['post'])
    def add_purchase_price(self, request, pk=None):
        """Alış fiyatı ekle"""
        part = self.get_object()
        price = request.data.get('price')
        quantity = request.data.get('quantity', 1)
        supplier = request.data.get('supplier', '')
        note = request.data.get('note', '')
        
        if not price:
            return Response(
                {'error': 'price gerekli'},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        purchase = PurchasePrice.objects.create(
            part=part,
            price=price,
            quantity=quantity,
            supplier=supplier,
            note=note,
            created_by=request.user
        )
        
        # Güncel alış fiyatını güncelle
        part.current_purchase_price = price
        part.save()
        
        serializer = PurchasePriceSerializer(purchase)
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    
    @action(detail=True, methods=['post'])
    def add_sale_price(self, request, pk=None):
        """Satış fiyatı ekle"""
        part = self.get_object()
        price = request.data.get('price')
        quantity = request.data.get('quantity', 1)
        customer = request.data.get('customer', '')
        note = request.data.get('note', '')
        
        if not price:
            return Response(
                {'error': 'price gerekli'},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        sale = SalePrice.objects.create(
            part=part,
            price=price,
            quantity=quantity,
            customer=customer,
            note=note,
            created_by=request.user
        )
        
        # Güncel satış fiyatını güncelle
        part.current_sale_price = price
        part.save()
        
        serializer = SalePriceSerializer(sale)
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    
    @action(detail=True, methods=['post'])
    def stock_movement(self, request, pk=None):
        """Stok hareketi"""
        part = self.get_object()
        movement_type = request.data.get('movement_type')
        quantity = request.data.get('quantity')
        note = request.data.get('note', '')
        
        if not movement_type or not quantity:
            return Response(
                {'error': 'movement_type ve quantity gerekli'},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        with transaction.atomic():
            # Stok hareketi kaydı oluştur
            movement = StockMovement.objects.create(
                part=part,
                movement_type=movement_type,
                quantity=quantity,
                note=note,
                created_by=request.user
            )
            
            # Stok miktarını güncelle
            if movement_type == 'purchase':
                part.quantity += int(quantity)
            elif movement_type == 'sale':
                if part.quantity < int(quantity):
                    return Response(
                        {'error': 'Yetersiz stok'},
                        status=status.HTTP_400_BAD_REQUEST
                    )
                part.quantity -= int(quantity)
            elif movement_type == 'return':
                part.quantity += int(quantity)
            elif movement_type == 'adjustment':
                # Manuel düzeltme - quantity direkt yeni miktar olarak kabul edilir
                part.quantity = int(quantity)
            
            part.save()
        
        serializer = StockMovementSerializer(movement)
        return Response(serializer.data, status=status.HTTP_201_CREATED)


class SearchViewSet(viewsets.ViewSet):
    """Google benzeri tek arama endpoint'i"""
    permission_classes = [IsAuthenticated, IsPremiumPro]
    
    @action(detail=False, methods=['get'])
    def search(self, request):
        """
        Google benzeri tek arama alanı
        Serbest yazı ile araç, parça adı, kategori ve usta notları içinde arama
        """
        query = request.query_params.get('q', '').strip()
        
        if not query:
            return Response(
                {'error': 'Arama sorgusu gerekli (q parametresi)'},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        # Kullanıcının workshop'larındaki parçalar
        user_parts = Part.objects.filter(workshop__owner=request.user)
        
        # Arama sorgusu
        search_query = Q(
            Q(name__icontains=query) |
            Q(code__icontains=query) |
            Q(auto_code__icontains=query) |
            Q(brand__icontains=query) |
            Q(category__name__icontains=query) |
            Q(category__subcategory__icontains=query) |
            Q(notes__note__icontains=query) |
            Q(compatibilities__vehicle__brand__icontains=query) |
            Q(compatibilities__vehicle__model__icontains=query) |
            Q(compatibilities__vehicle__engine__icontains=query)
        )
        
        parts = user_parts.filter(search_query).distinct()
        
        # Sonuçları formatla
        results = []
        for part in parts:
            # Uyumlu araçları getir
            vehicles = [comp.vehicle for comp in part.compatibilities.all()]
            
            results.append({
                'id': part.id,
                'name': part.name,
                'code': part.code,
                'auto_code': part.auto_code,
                'brand': part.brand,
                'category': part.category.name,
                'subcategory': part.category.subcategory,
                'quantity': part.quantity,
                'is_low_stock': part.is_low_stock,
                'current_purchase_price': str(part.current_purchase_price) if part.current_purchase_price else None,
                'current_sale_price': str(part.current_sale_price) if part.current_sale_price else None,
                'vehicles': [
                    {
                        'id': v.id,
                        'brand': v.brand,
                        'model': v.model,
                        'year_from': v.year_from,
                        'year_to': v.year_to,
                        'engine': v.engine,
                    }
                    for v in vehicles
                ],
                'image': part.image.url if part.image else None,
            })
        
        return Response({
            'query': query,
            'count': len(results),
            'results': results
        })


