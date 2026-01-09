from rest_framework import serializers
from .models import Conversation, Message


class MessageSerializer(serializers.ModelSerializer):
    sender_name = serializers.CharField(source='sender.first_name', read_only=True)
    
    class Meta:
        model = Message
        fields = ['id', 'sender', 'sender_name', 'content', 'is_read', 'created_at']
        read_only_fields = ['is_read', 'created_at']


class ConversationListSerializer(serializers.ModelSerializer):
    last_message = serializers.SerializerMethodField()
    workshop_name = serializers.CharField(source='workshop.name', read_only=True)
    customer_name = serializers.CharField(source='customer.first_name', read_only=True)
    
    class Meta:
        model = Conversation
        fields = ['id', 'workshop', 'workshop_name', 'customer', 'customer_name', 'last_message', 'updated_at']
    
    def get_last_message(self, obj):
        last_msg = obj.messages.last()
        if last_msg:
            return MessageSerializer(last_msg).data
        return None


class ConversationDetailSerializer(serializers.ModelSerializer):
    messages = MessageSerializer(many=True, read_only=True)
    workshop_name = serializers.CharField(source='workshop.name', read_only=True)
    customer_name = serializers.CharField(source='customer.first_name', read_only=True)
    
    class Meta:
        model = Conversation
        fields = ['id', 'workshop', 'workshop_name', 'customer', 'customer_name', 'messages', 'created_at']
