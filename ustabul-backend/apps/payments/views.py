from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from .models import PremiumPlan, Subscription, Invoice
from .serializers import PremiumPlanSerializer, SubscriptionSerializer, InvoiceSerializer


class PremiumPlanViewSet(viewsets.ReadOnlyModelViewSet):
    """Premium planları listeleme"""
    queryset = PremiumPlan.objects.filter(is_active=True)
    serializer_class = PremiumPlanSerializer


class SubscriptionViewSet(viewsets.ModelViewSet):
    """Abonelik yönetimi"""
    serializer_class = SubscriptionSerializer
    
    def get_queryset(self):
        if self.request.user.is_authenticated:
            return Subscription.objects.filter(user=self.request.user)
        return Subscription.objects.none()
    
    @action(detail=False, methods=['post'])
    def subscribe(self, request):
        """Premium planına abone olma"""
        plan_id = request.data.get('plan_id')
        
        if not plan_id:
            return Response(
                {'detail': 'Plan ID gerekli.'},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        try:
            plan = PremiumPlan.objects.get(id=plan_id)
        except PremiumPlan.DoesNotExist:
            return Response(
                {'detail': 'Plan bulunamadı.'},
                status=status.HTTP_404_NOT_FOUND
            )
        
        subscription = Subscription.objects.create(
            user=request.user,
            plan=plan,
            payment_method=request.data.get('payment_method', 'online')
        )
        
        # Kullanıcıyı premium yapma
        request.user.is_premium = True
        request.user.subscription_level = plan.level
        request.user.save()
        
        serializer = self.get_serializer(subscription)
        return Response(serializer.data, status=status.HTTP_201_CREATED)

    @action(detail=False, methods=['post'], permission_classes=[AllowAny])
    def webhook(self, request):
        """Ödeme sağlayıcıdan gelen webhook bildirimlerini işler"""
        # Gerçek uygulamada imza doğrulaması yapılmalı
        # event_type = request.data.get('type')
        # payload = request.data.get('payload')
        
        return Response({'status': 'received'})
    
    @action(detail=True, methods=['post'])
    def cancel(self, request, pk=None):
        """Aboneliği iptal etme"""
        subscription = self.get_object()
        subscription.status = 'cancelled'
        subscription.save()
        
        serializer = self.get_serializer(subscription)
        return Response(serializer.data)


class InvoiceViewSet(viewsets.ReadOnlyModelViewSet):
    """Fatura yönetimi"""
    serializer_class = InvoiceSerializer
    
    def get_queryset(self):
        if self.request.user.is_authenticated:
            return Invoice.objects.filter(subscription__user=self.request.user)
        return Invoice.objects.none()
