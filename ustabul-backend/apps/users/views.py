from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from django.contrib.auth import authenticate, login
from django.views.decorators.csrf import csrf_exempt
from .models import CustomUser, Favorite
from .serializers import CustomUserSerializer, CustomUserRegisterSerializer, FavoriteSerializer
import logging

logger = logging.getLogger(__name__)


class CustomUserViewSet(viewsets.ModelViewSet):
    """Kullanıcı yönetimi"""
    queryset = CustomUser.objects.all()
    serializer_class = CustomUserSerializer
    
    @csrf_exempt
    @action(detail=False, methods=['post'])
    def register(self, request):
        serializer = CustomUserRegisterSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.save()
            return Response({
                'id': user.id,
                'username': user.username,
                'email': user.email,
                'role': user.role,
                'message': 'Başarıyla kaydedildi!'
            }, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    @csrf_exempt
    @action(detail=False, methods=['post'], url_path='login')
    def login_view(self, request):
        try:
            username = request.data.get('username', '').strip()
            password = request.data.get('password', '').strip()
            
            # Gerekli alanları kontrol et
            if not username or not password:
                logger.warning('Username or password missing in login request')
                return Response(
                    {'detail': 'Kullanıcı adı ve şifre gereklidir.'},
                    status=status.HTTP_400_BAD_REQUEST
                )
            
            # Kullanıcıyı doğrula
            user = authenticate(username=username, password=password)
            if user is None:
                logger.warning(f'Authentication failed for username: {username}')
                return Response(
                    {'detail': 'Kullanıcı adı veya şifre yanlış.'},
                    status=status.HTTP_401_UNAUTHORIZED
                )
            
            # Session'a user'ı kaydet
            login(request, user)
            
            logger.info(f'User {username} logged in successfully.')
            return Response({
                'id': user.id,
                'username': user.username,
                'email': user.email,
                'role': user.role,
                'is_premium': user.is_premium,
                'message': 'Giriş başarılı!'
            }, status=status.HTTP_200_OK)
        except Exception as e:
            logger.error(f'Login error: {str(e)}')
            return Response(
                {'detail': 'Giriş işleminde hata oluştu.'},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )
    
    @action(detail=False, methods=['get', 'patch', 'put'])
    def me(self, request):
        logger.info(f'ME endpoint - Method: {request.method} - User authenticated: {request.user.is_authenticated}')
        
        if not request.user.is_authenticated:
            return Response({'detail': 'Kimlik doğrulaması gerekli.'}, status=status.HTTP_401_UNAUTHORIZED)

        if request.method == 'GET':
            serializer = self.get_serializer(request.user)
            return Response(serializer.data)
        
        elif request.method in ['PATCH', 'PUT']:
            serializer = self.get_serializer(request.user, data=request.data, partial=True)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    @action(detail=False, methods=['post'])
    def change_password(self, request):
        user = request.user
        old_password = request.data.get('old_password')
        new_password = request.data.get('new_password')
        
        if not user.check_password(old_password):
            return Response({'detail': 'Eski şifre yanlış.'}, status=status.HTTP_400_BAD_REQUEST)
        
        user.set_password(new_password)
        user.save()
        return Response({'detail': 'Şifre başarıyla değiştirildi.'})


class FavoriteViewSet(viewsets.ModelViewSet):
    """Favori yönetimi"""
    serializer_class = FavoriteSerializer
    
    def get_queryset(self):
        if self.request.user.is_authenticated:
            return Favorite.objects.filter(user=self.request.user)
        return Favorite.objects.none()
    
    def perform_create(self, serializer):
        serializer.save(user=self.request.user)
