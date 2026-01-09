"""
URL configuration for UstaBul project.
"""
from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from django.middleware.csrf import get_token
from django.http import JsonResponse

def get_csrf_token(request):
    """CSRF token'ı frontend'e gönder"""
    token = get_token(request)
    return JsonResponse({'csrfToken': token})

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/csrf-token/', get_csrf_token, name='csrf_token'),
    path('api/users/', include('apps.users.urls')),
    path('api/workshops/', include('apps.workshops.urls')),
    path('api/reviews/', include('apps.reviews.urls')),
    path('api/messaging/', include('apps.messaging.urls')),
    path('api/inventory/', include('apps.inventory.urls')),
    path('api/payments/', include('apps.payments.urls')),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
