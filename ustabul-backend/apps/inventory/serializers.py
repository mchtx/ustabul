from rest_framework import serializers
from .models import (
    Vehicle, PartCategory, Part, PartCompatibility, 
    AlternativePart, PartNote, PurchasePrice, 
    SalePrice, StockMovement
)
from apps.workshops.models import Workshop


class VehicleSerializer(serializers.ModelSerializer):
    class Meta:
        model = Vehicle
        fields = ['id', 'brand', 'model', 'year_from', 'year_to', 'engine', 'engine_code']
        read_only_fields = ['id']


class PartCategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = PartCategory
        fields = ['id', 'name', 'subcategory', 'is_active']
        read_only_fields = ['id']


class PartCompatibilitySerializer(serializers.ModelSerializer):
    vehicle_details = VehicleSerializer(source='vehicle', read_only=True)
    
    class Meta:
        model = PartCompatibility
        fields = ['id', 'vehicle', 'vehicle_details']
        read_only_fields = ['id']


class AlternativePartSerializer(serializers.ModelSerializer):
    alternative_details = serializers.SerializerMethodField()
    
    class Meta:
        model = AlternativePart
        fields = ['id', 'alternative', 'alternative_details', 'note']
        read_only_fields = ['id']
    
    def get_alternative_details(self, obj):
        return {
            'id': obj.alternative.id,
            'name': obj.alternative.name,
            'code': obj.alternative.code,
            'auto_code': obj.alternative.auto_code,
            'category': obj.alternative.category.name,
        }


class PartNoteSerializer(serializers.ModelSerializer):
    created_by_name = serializers.CharField(source='created_by.get_full_name', read_only=True)
    created_by_username = serializers.CharField(source='created_by.username', read_only=True)
    
    class Meta:
        model = PartNote
        fields = ['id', 'note', 'created_by_name', 'created_by_username', 'created_at']
        read_only_fields = ['id', 'created_at']


class PurchasePriceSerializer(serializers.ModelSerializer):
    created_by_name = serializers.CharField(source='created_by.get_full_name', read_only=True)
    
    class Meta:
        model = PurchasePrice
        fields = [
            'id', 'price', 'quantity', 'supplier', 'note', 
            'created_by_name', 'created_at'
        ]
        read_only_fields = ['id', 'created_at']


class SalePriceSerializer(serializers.ModelSerializer):
    created_by_name = serializers.CharField(source='created_by.get_full_name', read_only=True)
    
    class Meta:
        model = SalePrice
        fields = [
            'id', 'price', 'quantity', 'customer', 'note',
            'created_by_name', 'created_at'
        ]
        read_only_fields = ['id', 'created_at']


class StockMovementSerializer(serializers.ModelSerializer):
    created_by_name = serializers.CharField(source='created_by.get_full_name', read_only=True)
    
    class Meta:
        model = StockMovement
        fields = [
            'id', 'movement_type', 'quantity', 'note',
            'created_by_name', 'created_at'
        ]
        read_only_fields = ['id', 'created_at']


class PartSerializer(serializers.ModelSerializer):
    """Parça serializer - detaylı"""
    category_name = serializers.CharField(source='category.name', read_only=True)
    category_subcategory = serializers.CharField(source='category.subcategory', read_only=True)
    is_low_stock = serializers.BooleanField(read_only=True)
    average_purchase_price = serializers.DecimalField(max_digits=10, decimal_places=2, read_only=True)
    profit_percentage = serializers.DecimalField(max_digits=5, decimal_places=2, read_only=True)
    
    # İlişkili veriler
    compatibilities = PartCompatibilitySerializer(many=True, read_only=True)
    alternatives = AlternativePartSerializer(many=True, read_only=True)
    notes = PartNoteSerializer(many=True, read_only=True)
    purchase_prices = PurchasePriceSerializer(many=True, read_only=True)
    sale_prices = SalePriceSerializer(many=True, read_only=True)
    movements = StockMovementSerializer(many=True, read_only=True)
    
    class Meta:
        model = Part
        fields = [
            'id', 'name', 'category', 'category_name', 'category_subcategory',
            'brand', 'code', 'auto_code', 'image',
            'quantity', 'min_stock', 'is_low_stock',
            'current_purchase_price', 'current_sale_price',
            'average_purchase_price', 'profit_percentage',
            'is_active', 'created_at', 'updated_at',
            'compatibilities', 'alternatives', 'notes',
            'purchase_prices', 'sale_prices', 'movements'
        ]
        read_only_fields = [
            'id', 'auto_code', 'created_at', 'updated_at',
            'is_low_stock', 'average_purchase_price', 'profit_percentage'
        ]


class PartListSerializer(serializers.ModelSerializer):
    """Parça listesi için basit serializer"""
    category_name = serializers.CharField(source='category.name', read_only=True)
    category_subcategory = serializers.CharField(source='category.subcategory', read_only=True)
    is_low_stock = serializers.BooleanField(read_only=True)
    vehicle_count = serializers.IntegerField(source='compatibilities.count', read_only=True)
    
    class Meta:
        model = Part
        fields = [
            'id', 'name', 'category_name', 'category_subcategory',
            'brand', 'code', 'auto_code',
            'quantity', 'min_stock', 'is_low_stock',
            'current_purchase_price', 'current_sale_price',
            'vehicle_count', 'is_active'
        ]


class PartCreateSerializer(serializers.ModelSerializer):
    """Parça oluşturma için serializer"""
    vehicle_ids = serializers.ListField(
        child=serializers.IntegerField(),
        write_only=True,
        required=False,
        help_text="Uyumlu araç ID'leri listesi"
    )
    
    class Meta:
        model = Part
        fields = [
            'name', 'category', 'brand', 'code', 'image',
            'quantity', 'min_stock',
            'current_purchase_price', 'current_sale_price',
            'vehicle_ids'
        ]
        extra_kwargs = {
            'name': {'required': False, 'allow_blank': True},
            'category': {'required': False, 'allow_null': True},
            'brand': {'required': False, 'allow_blank': True},
            'code': {'required': False, 'allow_blank': True},
            'image': {'required': False, 'allow_null': True},
            'quantity': {'required': False},
            'min_stock': {'required': False},
            'current_purchase_price': {'required': False, 'allow_null': True},
            'current_sale_price': {'required': False, 'allow_null': True},
        }
    
    def create(self, validated_data):
        vehicle_ids = validated_data.pop('vehicle_ids', [])
        
        # Eğer category sağlanmadıysa, default category'yi al veya oluştur
        if 'category' not in validated_data or validated_data.get('category') is None:
            default_category = PartCategory.objects.first()
            if not default_category:
                default_category = PartCategory.objects.create(name='Genel')
            validated_data['category'] = default_category
        
        # Eğer name sağlanmadıysa, default name ver
        if not validated_data.get('name'):
            validated_data['name'] = "Belirtilmemiş Parça"

        # Eğer workshop sağlanmadıysa, isteği yapan kullanıcının dükkanını kullan veya oluştur
        if 'workshop' not in validated_data or validated_data.get('workshop') is None:
            request = self.context.get('request') if hasattr(self, 'context') else None
            user = getattr(request, 'user', None) if request is not None else None
            if user and user.is_authenticated:
                ws = Workshop.objects.filter(owner=user).first()
                if not ws:
                    ws = Workshop.objects.create(
                        owner=user,
                        name=f"{user.username} - Auto Workshop",
                        address='-',
                        phone='000',
                        district='-'
                    )
                validated_data['workshop'] = ws
        
        part = Part.objects.create(**validated_data)
        
        # Araç uyumluluklarını ekle
        for vehicle_id in vehicle_ids:
            try:
                vehicle = Vehicle.objects.get(id=vehicle_id)
                PartCompatibility.objects.create(part=part, vehicle=vehicle)
            except Vehicle.DoesNotExist:
                pass
        
        return part
