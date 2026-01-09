from rest_framework import serializers
from .models import PremiumPlan, Subscription, Invoice


class PremiumPlanSerializer(serializers.ModelSerializer):
    class Meta:
        model = PremiumPlan
        fields = ['id', 'name', 'description', 'duration_days', 'price', 'features']


class SubscriptionSerializer(serializers.ModelSerializer):
    plan_name = serializers.CharField(source='plan.name', read_only=True)
    is_active = serializers.BooleanField(read_only=True)
    
    class Meta:
        model = Subscription
        fields = ['id', 'plan', 'plan_name', 'start_date', 'end_date', 'status', 'is_active']


class InvoiceSerializer(serializers.ModelSerializer):
    class Meta:
        model = Invoice
        fields = ['id', 'invoice_number', 'amount', 'status', 'issued_at', 'due_date', 'paid_at']
        read_only_fields = ['invoice_number', 'issued_at']
