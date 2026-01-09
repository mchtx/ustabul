from rest_framework import serializers
from .models import Review, ReviewReply


class ReviewReplySerializer(serializers.ModelSerializer):
    workshop_owner_name = serializers.CharField(source='workshop_owner.first_name', read_only=True)
    
    class Meta:
        model = ReviewReply
        fields = ['id', 'workshop_owner_name', 'comment', 'created_at', 'updated_at']


class ReviewSerializer(serializers.ModelSerializer):
    user_name = serializers.SerializerMethodField(read_only=True)
    user_id = serializers.IntegerField(source='user.id', read_only=True)
    workshop_name = serializers.CharField(source='workshop.name', read_only=True)
    workshop_category_name = serializers.CharField(source='workshop.category.name', read_only=True)
    replies = ReviewReplySerializer(source='reply', many=True, read_only=True)
    
    def get_user_name(self, obj):
        """Kullanıcı adını getir - boşsa username kullan"""
        if obj.user.first_name:
            return obj.user.first_name
        return obj.user.username
    
    class Meta:
        model = Review
        fields = ['id', 'user_id', 'user_name', 'workshop_name', 'workshop_category_name', 'rating', 'comment', 'is_verified', 'is_approved', 'replies', 'created_at']
        read_only_fields = ['is_verified', 'is_approved', 'created_at']


class ReviewCreateUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Review
        fields = ['rating', 'comment']
    
    def create(self, validated_data):
        return Review.objects.create(**validated_data)
