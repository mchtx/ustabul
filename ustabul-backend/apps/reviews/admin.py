from django.contrib import admin
from .models import Review, ReviewReply


@admin.register(Review)
class ReviewAdmin(admin.ModelAdmin):
    list_display = ['user', 'workshop', 'rating', 'is_approved', 'created_at']
    list_filter = ['rating', 'is_approved', 'created_at']
    search_fields = ['user__username', 'workshop__name', 'comment']
    readonly_fields = ['created_at', 'updated_at']


@admin.register(ReviewReply)
class ReviewReplyAdmin(admin.ModelAdmin):
    list_display = ['review', 'workshop_owner', 'created_at']
    list_filter = ['created_at']
    search_fields = ['review__workshop__name', 'workshop_owner__username']
    readonly_fields = ['created_at', 'updated_at']
