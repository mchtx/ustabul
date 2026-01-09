from django.contrib import admin
from .models import (
    Vehicle, PartCategory, Part, PartCompatibility,
    AlternativePart, PartNote, PurchasePrice,
    SalePrice, StockMovement
)


@admin.register(Vehicle)
class VehicleAdmin(admin.ModelAdmin):
    list_display = ['brand', 'model', 'year_from', 'year_to', 'engine']
    list_filter = ['brand', 'year_from']
    search_fields = ['brand', 'model', 'engine', 'engine_code']
    ordering = ['brand', 'model', 'year_from']


@admin.register(PartCategory)
class PartCategoryAdmin(admin.ModelAdmin):
    list_display = ['name', 'subcategory', 'is_active']
    list_filter = ['name', 'is_active']
    search_fields = ['name', 'subcategory']
    ordering = ['name', 'subcategory']


@admin.register(Part)
class PartAdmin(admin.ModelAdmin):
    list_display = ['name', 'workshop', 'category', 'quantity', 'min_stock', 'is_low_stock', 'is_active']
    list_filter = ['workshop', 'category', 'is_active', 'created_at']
    search_fields = ['name', 'code', 'auto_code', 'brand', 'workshop__name']
    readonly_fields = ['auto_code', 'created_at', 'updated_at']
    filter_horizontal = []
    
    fieldsets = (
        ('Temel Bilgiler', {
            'fields': ('workshop', 'name', 'category', 'auto_code')
        }),
        ('Opsiyonel Bilgiler', {
            'fields': ('brand', 'code', 'image')
        }),
        ('Stok', {
            'fields': ('quantity', 'min_stock')
        }),
        ('Fiyat', {
            'fields': ('current_purchase_price', 'current_sale_price')
        }),
        ('Durum', {
            'fields': ('is_active', 'created_at', 'updated_at')
        }),
    )


@admin.register(PartCompatibility)
class PartCompatibilityAdmin(admin.ModelAdmin):
    list_display = ['part', 'vehicle']
    list_filter = ['vehicle__brand', 'vehicle__model']
    search_fields = ['part__name', 'vehicle__brand', 'vehicle__model']


@admin.register(AlternativePart)
class AlternativePartAdmin(admin.ModelAdmin):
    list_display = ['part', 'alternative', 'note']
    search_fields = ['part__name', 'alternative__name']


@admin.register(PartNote)
class PartNoteAdmin(admin.ModelAdmin):
    list_display = ['part', 'created_by', 'created_at']
    list_filter = ['created_at']
    search_fields = ['part__name', 'note', 'created_by__username']
    readonly_fields = ['created_at']


@admin.register(PurchasePrice)
class PurchasePriceAdmin(admin.ModelAdmin):
    list_display = ['part', 'price', 'quantity', 'supplier', 'created_at']
    list_filter = ['created_at']
    search_fields = ['part__name', 'supplier']
    readonly_fields = ['created_at']


@admin.register(SalePrice)
class SalePriceAdmin(admin.ModelAdmin):
    list_display = ['part', 'price', 'quantity', 'customer', 'created_at']
    list_filter = ['created_at']
    search_fields = ['part__name', 'customer']
    readonly_fields = ['created_at']


@admin.register(StockMovement)
class StockMovementAdmin(admin.ModelAdmin):
    list_display = ['part', 'movement_type', 'quantity', 'created_by', 'created_at']
    list_filter = ['movement_type', 'created_at']
    search_fields = ['part__name', 'created_by__username', 'note']
    readonly_fields = ['created_at']
