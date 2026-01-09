from rest_framework import viewsets, status
from rest_framework.decorators import action, api_view
from rest_framework.response import Response
from rest_framework.authentication import SessionAuthentication
from rest_framework.permissions import AllowAny
from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator
from .models import Review, ReviewReply
from .serializers import ReviewSerializer, ReviewCreateUpdateSerializer, ReviewReplySerializer
import logging
import requests

logger = logging.getLogger(__name__)


class ReviewViewSet(viewsets.ModelViewSet):
    """Yorum yönetimi"""
    serializer_class = ReviewSerializer
    authentication_classes = [SessionAuthentication]
    permission_classes = [AllowAny]
    
    def get_queryset(self):
        queryset = Review.objects.all().order_by('-created_at')
        workshop_id = self.request.query_params.get('workshop')
        if workshop_id:
            queryset = queryset.filter(workshop_id=workshop_id)
        # Onaylı olmayan review'ları show et (profil sayfasında ihtiyaç için)
        return queryset
    
    def get_serializer_class(self):
        if self.action in ['create', 'update', 'partial_update']:
            return ReviewCreateUpdateSerializer
        return ReviewSerializer
    
    def create(self, request, *args, **kwargs):
        try:
            logger.info(f'Review create attempt - User: {request.user}')
            logger.info(f'Review create attempt - Is authenticated: {request.user.is_authenticated}')
            
            # Giriş kontrolü
            if not request.user.is_authenticated:
                logger.warning('Unauthenticated attempt to create review')
                return Response(
                    {'detail': 'Yorum yapmak için giriş yapmalısınız.'},
                    status=status.HTTP_401_UNAUTHORIZED
                )
            
            workshop_id = request.query_params.get('workshop')
            if not workshop_id:
                logger.warning(f'Review creation attempt without workshop_id by user {request.user.id}')
                return Response(
                    {'detail': 'Workshop ID gerekli.'},
                    status=status.HTTP_400_BAD_REQUEST
                )
            
            logger.info(f'User {request.user.username} creating review for workshop {workshop_id}')
            
            # Serializer'a veri gönder
            serializer = self.get_serializer(data=request.data)
            if serializer.is_valid():
                # user ve workshop_id'yi save metoduna geç
                serializer.save(user=request.user, workshop_id=workshop_id)
                logger.info(f'Review created successfully by {request.user.username} for workshop {workshop_id}')
                return Response(serializer.data, status=status.HTTP_201_CREATED)
            
            logger.warning(f'Review creation failed: {serializer.errors}')
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            logger.error(f'Review creation error: {str(e)}', exc_info=True)
            return Response(
                {'detail': 'Yorum oluşturma işleminde hata oluştu.'},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )
    
    @action(detail=True, methods=['post'])
    def reply(self, request, pk=None):
        """İşletme yanıt yazma"""
        review = self.get_object()
        
        # Sadece ilgili işletme sahibi yanıt yazabilir
        if review.workshop.owner != request.user:
            return Response(
                {'detail': 'Yalnızca işletme sahibi yanıt yazabilir.'},
                status=status.HTTP_403_FORBIDDEN
            )
        
        serializer = ReviewReplySerializer(data=request.data)
        if serializer.is_valid():
            serializer.save(review=review, workshop_owner=request.user)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['POST'])
def ai_chat(request):
    """AI Asistan Chat API - HuggingFace"""
    try:
        message = request.data.get('message', '').strip()
        if not message:
            return Response(
                {'error': 'Mesaj gerekli'},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        api_url = "https://router.huggingface.co/v1/chat/completions"
        huggingface_token = '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'
        
        logger.info(f'AI Chat Request: {message[:100]}')
        
        try:
            response = requests.post(
                api_url,
                headers={
                    "Authorization": f"Bearer {huggingface_token}",
                    "Content-Type": "application/json"
                },
                json={
                    "model": "meta-llama/Meta-Llama-3-8B-Instruct",
                    "messages": [
                        {
                            "role": "system",
                            "content": "Sen UstaBul uygulamasının Türkçe yardımcı asistanısın. Adıyaman'da ustalar bulma, dükkanları inceleme, randevu alma ve platform hakkında sorularda yardımcı olursun. Kısa ve anlaşılır cevaplar ver. Türkçe olarak yanıt ver."
                        },
                        {
                            "role": "user",
                            "content": message
                        }
                    ],
                    "temperature": 0.7,
                    "max_tokens": 300
                },
                timeout=60
            )
            
            logger.info(f'HuggingFace Response Status: {response.status_code}')
            logger.info(f'HuggingFace Response Text: {response.text[:200]}')
            
            # Boş yanıt kontrolü
            if not response.text:
                logger.error('Empty response from HuggingFace')
                return Response(
                    {'error': 'API boş yanıt verdi. Model yükleniyor olabilir, lütfen 30 saniye bekleyin.'},
                    status=status.HTTP_503_SERVICE_UNAVAILABLE
                )
            
            if response.status_code != 200:
                logger.error(f'HuggingFace API Error Status: {response.status_code}')
                logger.error(f'HuggingFace API Error Text: {response.text}')
                return Response(
                    {'error': f'HuggingFace Hatası: {response.status_code}'},
                    status=status.HTTP_500_INTERNAL_SERVER_ERROR
                )
            
            try:
                data = response.json()
            except Exception as json_error:
                logger.error(f'JSON Parse Error: {str(json_error)}, Response: {response.text}')
                return Response(
                    {'error': f'API yanıtı işlenemedi: {str(json_error)}'},
                    status=status.HTTP_500_INTERNAL_SERVER_ERROR
                )
            
            logger.info(f'HuggingFace Response Data: {data}')
            
            # Chat completions formatında yanıt işleme
            if 'choices' in data and len(data['choices']) > 0:
                bot_reply = data['choices'][0]['message']['content']
                logger.info(f'AI Chat Response: {bot_reply[:100]}')
                return Response({'reply': bot_reply})
            
            if 'error' in data:
                logger.error(f'API Error in response: {data["error"]}')
                return Response(
                    {'error': f'API Hatası: {data["error"]}'},
                    status=status.HTTP_500_INTERNAL_SERVER_ERROR
                )
            
            logger.error(f'Unexpected API format: {data}')
            return Response(
                {'error': 'Yanıt işlenemedi'},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )
        
        except requests.exceptions.Timeout:
            logger.error('HuggingFace API timeout')
            return Response(
                {'error': 'İstek zaman aşımına uğradı. Model başlıyor olabilir, lütfen 30 saniye bekleyin ve tekrar deneyin.'},
                status=status.HTTP_504_GATEWAY_TIMEOUT
            )
        except requests.exceptions.ConnectionError as e:
            logger.error(f'Connection error: {str(e)}')
            return Response(
                {'error': 'Bağlantı hatası. İnternet bağlantınızı kontrol edin.'},
                status=status.HTTP_503_SERVICE_UNAVAILABLE
            )
        except Exception as e:
            logger.error(f'Request error: {str(e)}', exc_info=True)
            return Response(
                {'error': f'İstek hatası: {str(e)}'},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )
    
    except Exception as e:
        logger.error(f'AI Assistant error: {str(e)}', exc_info=True)
        return Response(
            {'error': f'Hata: {str(e)}'},
            status=status.HTTP_500_INTERNAL_SERVER_ERROR
        )
