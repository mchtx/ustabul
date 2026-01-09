from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.authentication import SessionAuthentication, BasicAuthentication
from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator
from django.db import models
from .models import Conversation, Message
from .serializers import ConversationListSerializer, ConversationDetailSerializer, MessageSerializer


@method_decorator(csrf_exempt, name='dispatch')
class ConversationViewSet(viewsets.ModelViewSet):
    """Sohbet yönetimi"""
    serializer_class = ConversationListSerializer
    
    def get_queryset(self):
        user = self.request.user
        if not user.is_authenticated:
            return Conversation.objects.none()
        
        # Kullanıcı ya müşteri ya da işletme sahibi olabilir
        return Conversation.objects.filter(
            models.Q(customer=user) | models.Q(workshop__owner=user)
        ).distinct()
    
    def get_serializer_class(self):
        if self.action == 'retrieve':
            return ConversationDetailSerializer
        return ConversationListSerializer
    
    @action(detail=False, methods=['post'])
    def start_conversation(self, request):
        """Yeni sohbet başlatma"""
        # Giriş kontrolü
        if not request.user.is_authenticated:
            return Response(
                {'detail': 'Sohbet başlatmak için giriş yapmalısınız.'},
                status=status.HTTP_401_UNAUTHORIZED
            )
        
        workshop_id = request.data.get('workshop_id')
        
        if not workshop_id:
            return Response(
                {'detail': 'Workshop ID gerekli.'},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        conversation, created = Conversation.objects.get_or_create(
            customer=request.user,
            workshop_id=workshop_id
        )
        
        serializer = ConversationDetailSerializer(conversation)
        return Response(serializer.data, status=status.HTTP_201_CREATED if created else status.HTTP_200_OK)
    
    @action(detail=True, methods=['post'])
    def send_message(self, request, pk=None):
        """Mesaj gönderme"""
        # Giriş kontrolü
        if not request.user.is_authenticated:
            return Response(
                {'detail': 'Mesaj göndermek için giriş yapmalısınız.'},
                status=status.HTTP_401_UNAUTHORIZED
            )
        
        conversation = self.get_object()
        
        # Kullanıcının bu sohbete erişim yetkisi var mı kontrol et
        if conversation.customer != request.user and conversation.workshop.owner != request.user:
            return Response(
                {'detail': 'Bu sohbete mesaj gönderme yetkiniz yok.'},
                status=status.HTTP_403_FORBIDDEN
            )
        
        content = request.data.get('content')
        
        if not content:
            return Response(
                {'detail': 'Mesaj içeriği gerekli.'},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        message = Message.objects.create(
            conversation=conversation,
            sender=request.user,
            content=content
        )
        
        serializer = MessageSerializer(message)
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    
    @action(detail=True, methods=['post'])
    def mark_as_read(self, request, pk=None):
        """Okunmamış mesajları okundu işaretle"""
        conversation = self.get_object()
        conversation.messages.filter(is_read=False).exclude(sender=request.user).update(is_read=True)
        
        serializer = ConversationDetailSerializer(conversation)
        return Response(serializer.data)

