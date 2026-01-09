from django.contrib import admin
from .models import CustomUser, Favorite


@admin.register(CustomUser)
class CustomUserAdmin(admin.ModelAdmin):
    list_display = ['username', 'email', 'role', 'is_premium', 'is_banned', 'created_at']
    list_filter = ['role', 'is_premium', 'is_banned', 'created_at']
    search_fields = ['username', 'email', 'first_name', 'last_name']
    ordering = ['-created_at']


@admin.register(Favorite)
class FavoriteAdmin(admin.ModelAdmin):
    list_display = ['user', 'workshop', 'created_at']
    list_filter = ['created_at']
    search_fields = ['user__username', 'workshop__name']
