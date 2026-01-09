from rest_framework import serializers
from .models import CustomUser, Favorite


class CustomUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        fields = ['id', 'username', 'email', 'first_name', 'last_name', 'phone', 'role', 'is_premium', 'subscription_level', 'created_at', 'profile_picture']
        read_only_fields = ['created_at']


class CustomUserRegisterSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True, min_length=6)
    password_confirm = serializers.CharField(write_only=True, min_length=6)
    id = serializers.IntegerField(read_only=True)
    
    class Meta:
        model = CustomUser
        fields = ['id', 'username', 'email', 'password', 'password_confirm', 'first_name', 'last_name', 'phone', 'role']
    
    def validate(self, data):
        if data['password'] != data.pop('password_confirm'):
            raise serializers.ValidationError('Şifreler eşleşmiyor.')
        return data
    
    def create(self, validated_data):
        # Role alanını ayrı al
        role = validated_data.pop('role', 'customer')
        user = CustomUser.objects.create_user(**validated_data)
        user.role = role
        user.save()
        return user


class FavoriteSerializer(serializers.ModelSerializer):
    workshop_name = serializers.CharField(source='workshop.name', read_only=True)
    
    class Meta:
        model = Favorite
        fields = ['id', 'workshop', 'workshop_name', 'created_at']
        read_only_fields = ['created_at']
