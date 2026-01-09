from django.contrib import admin
from .models import Category, Workshop, WorkingHours, Service


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ['name', 'created_at']
    search_fields = ['name']


@admin.register(Workshop)
class WorkshopAdmin(admin.ModelAdmin):
    list_display = ['name', 'owner', 'category', 'district', 'is_premium', 'is_active', 'average_rating']
    list_filter = ['category', 'district', 'is_premium', 'is_active', 'created_at']
    search_fields = ['name', 'owner__username', 'address']
    readonly_fields = ['average_rating', 'total_reviews', 'created_at', 'updated_at']


@admin.register(WorkingHours)
class WorkingHoursAdmin(admin.ModelAdmin):
    list_display = ['workshop', 'day_of_week', 'opening_time', 'closing_time', 'is_closed']
    list_filter = ['day_of_week', 'is_closed']
    search_fields = ['workshop__name']


@admin.register(Service)
class ServiceAdmin(admin.ModelAdmin):
    list_display = ['workshop', 'name', 'price']
    list_filter = ['workshop']
    search_fields = ['name', 'workshop__name']
