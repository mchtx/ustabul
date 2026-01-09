from rest_framework import serializers
from django.db.models import Avg, Count
from .models import Category, Workshop, WorkingHours, Service


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ['id', 'name', 'description', 'icon']


class WorkingHoursSerializer(serializers.ModelSerializer):
    day_display = serializers.CharField(source='get_day_of_week_display', read_only=True)
    
    class Meta:
        model = WorkingHours
        fields = ['id', 'day_of_week', 'day_display', 'opening_time', 'closing_time', 'is_closed']


class ServiceSerializer(serializers.ModelSerializer):
    class Meta:
        model = Service
        fields = ['id', 'name', 'description', 'price']


class WorkshopListSerializer(serializers.ModelSerializer):
    category_name = serializers.CharField(source='category.name', read_only=True)
    average_rating = serializers.SerializerMethodField()
    total_reviews = serializers.SerializerMethodField()
    
    class Meta:
        model = Workshop
        fields = [
            'id', 'name', 'category', 'category_name', 'district', 'phone',
            'image', 'average_rating', 'total_reviews', 'is_premium', 'is_active'
        ]
    
    def get_average_rating(self, obj):
        """Dinamik olarak yorumlardan ortalama puanı hesapla"""
        avg_rating = obj.reviews.filter(is_approved=True).aggregate(avg=Avg('rating'))['avg']
        return round(avg_rating, 1) if avg_rating else 0.0
    
    def get_total_reviews(self, obj):
        """Dinamik olarak onaylanmış yorum sayısını hesapla"""
        return obj.reviews.filter(is_approved=True).count()


class WorkshopDetailSerializer(serializers.ModelSerializer):
    category_name = serializers.CharField(source='category.name', read_only=True)
    working_hours = WorkingHoursSerializer(many=True, read_only=True)
    services = ServiceSerializer(many=True, read_only=True)
    average_rating = serializers.SerializerMethodField()
    total_reviews = serializers.SerializerMethodField()
    
    class Meta:
        model = Workshop
        fields = [
            'id', 'name', 'category', 'category_name', 'description', 'address',
            'phone', 'whatsapp', 'email', 'city', 'district', 'neighborhood',
            'image', 'average_rating', 'total_reviews', 'is_active', 'is_premium',
            'is_closed_today', 'closed_today_reason', 'working_hours', 'services',
            'created_at', 'updated_at'
        ]
        read_only_fields = ['created_at', 'updated_at', 'average_rating', 'total_reviews']
    
    def get_average_rating(self, obj):
        """Dinamik olarak yorumlardan ortalama puanı hesapla"""
        avg_rating = obj.reviews.filter(is_approved=True).aggregate(avg=Avg('rating'))['avg']
        return round(avg_rating, 1) if avg_rating else 0.0
    
    def get_total_reviews(self, obj):
        """Dinamik olarak onaylanmış yorum sayısını hesapla"""
        return obj.reviews.filter(is_approved=True).count()
