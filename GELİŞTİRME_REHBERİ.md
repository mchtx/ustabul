# UstaBul Projesi - Geliştirme Rehberi

## 📚 İçindekiler

1. [Backend Geliştirmesi](#backend-geliştirmesi)
2. [Frontend Geliştirmesi](#frontend-geliştirmesi)
3. [Database Modelleri](#database-modelleri)
4. [API İşlemi Akışı](#api-işlemi-akışı)
5. [Authentikasyon](#authentikasyon)

---

## Backend Geliştirmesi

### Django Proje Yapısı

```
ustabul-backend/
├── config/                  # Proje ayarları
│   ├── settings.py         # Django ayarları
│   ├── urls.py             # URL routing
│   ├── wsgi.py
│   └── asgi.py
├── apps/
│   ├── users/
│   │   ├── models.py       # Kullanıcı modelleri
│   │   ├── serializers.py  # JSON dönüşüm
│   │   ├── views.py        # İş mantığı
│   │   ├── urls.py         # Rota tanımı
│   │   └── admin.py        # Admin paneli
│   ├── workshops/          # Dükkan uygulaması
│   ├── reviews/            # Yorum uygulaması
│   ├── messaging/          # Mesajlaşma uygulaması
│   ├── inventory/          # Stok uygulaması
│   └── payments/           # Ödeme uygulaması
├── manage.py
└── requirements.txt
```

### Yeni App Ekleme

```bash
python manage.py startapp app_name apps/app_name
```

Sonra `config/settings.py` içinde INSTALLED_APPS'e ekleyin:
```python
INSTALLED_APPS = [
    ...
    'apps.app_name',
]
```

### Model Oluşturma

`apps/your_app/models.py`:
```python
from django.db import models

class YourModel(models.Model):
    name = models.CharField(max_length=100, verbose_name='Ad')
    description = models.TextField(blank=True, verbose_name='Açıklama')
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        verbose_name = 'Model Adı'
        verbose_name_plural = 'Model Adları'
        ordering = ['-created_at']
    
    def __str__(self):
        return self.name
```

### Migration Yapma

```bash
python manage.py makemigrations
python manage.py migrate
```

### Serializer Oluşturma

`apps/your_app/serializers.py`:
```python
from rest_framework import serializers
from .models import YourModel

class YourModelSerializer(serializers.ModelSerializer):
    class Meta:
        model = YourModel
        fields = ['id', 'name', 'description', 'created_at']
        read_only_fields = ['created_at']
```

### ViewSet Oluşturma

`apps/your_app/views.py`:
```python
from rest_framework import viewsets
from .models import YourModel
from .serializers import YourModelSerializer

class YourModelViewSet(viewsets.ModelViewSet):
    queryset = YourModel.objects.all()
    serializer_class = YourModelSerializer
```

### URL Routing

`apps/your_app/urls.py`:
```python
from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import YourModelViewSet

router = DefaultRouter()
router.register(r'', YourModelViewSet, basename='yourmodel')

urlpatterns = [
    path('', include(router.urls)),
]
```

Ana `config/urls.py` içine ekleyin:
```python
urlpatterns = [
    path('api/yourapp/', include('apps.your_app.urls')),
]
```

---

## Frontend Geliştirmesi

### Sayfa Oluşturma

`src/pages/YourPage.js`:
```javascript
import React, { useState, useEffect } from 'react';
import { useAuth } from '../hooks';

function YourPage() {
  const { user } = useAuth();
  const [data, setData] = useState([]);
  const [isLoading, setIsLoading] = useState(true);

  useEffect(() => {
    fetchData();
  }, []);

  const fetchData = async () => {
    try {
      // API çağrısı
      setIsLoading(false);
    } catch (error) {
      console.error('Hata:', error);
    }
  };

  if (isLoading) return <div>Yükleniyor...</div>;

  return (
    <div>
      {/* İçerik */}
    </div>
  );
}

export default YourPage;
```

### Bileşen Oluşturma

`src/components/YourComponent.js`:
```javascript
import React from 'react';

function YourComponent({ data, onAction }) {
  return (
    <div className="bg-white p-4 rounded-lg shadow">
      {/* Bileşen içeriği */}
    </div>
  );
}

export default YourComponent;
```

### API Çağrısı Yapma

`src/api.js` içine yeni endpoint ekleyin:
```javascript
export const yourAPI = {
  getItems: () => api.get('/yourapp/'),
  getItem: (id) => api.get(`/yourapp/${id}/`),
  createItem: (data) => api.post('/yourapp/', data),
  updateItem: (id, data) => api.patch(`/yourapp/${id}/`, data),
  deleteItem: (id) => api.delete(`/yourapp/${id}/`),
};
```

Sayfada kullanın:
```javascript
import { yourAPI } from '../api';

const fetchData = async () => {
  try {
    const response = await yourAPI.getItems();
    setData(response.data);
  } catch (error) {
    console.error('Hata:', error);
  }
};
```

### Router Ekleme

`src/App.js` içinde:
```javascript
<Routes>
  <Route path="/yourpath" element={<YourPage />} />
</Routes>
```

---

## Database Modelleri

### Kullanıcı Modeli
```python
# Roller: customer, workshop, parts_dealer, admin
# Premium üyelik kontrolü
# Yasaklama sistemi
```

### Workshop Modeli
```python
# İlişkiler: Owner (User), Category
# Konum bilgileri (latitude, longitude)
# Çalışma saatleri
# Ortalama puan ve yorum sayısı
# Premium status
```

### Review Modeli
```python
# İlişkiler: User (yorum yapan), Workshop (yapılan yorum)
# 1-5 puan sistemi
# Yorum metni
# İşletme yanıtı (ReviewReply)
```

### Conversation Modeli
```python
# İlişkiler: Customer (User), Workshop
# Mesajlar (Message) ile ilişki
# Aktiflik durumu
```

### Product Modeli (Inventory)
```python
# İlişkiler: Workshop
# Stok miktarı ve minimum stok
# Fiyat ve maliyet
# Tedarikçi bilgileri
# Resim
```

### Subscription Modeli (Payments)
```python
# İlişkiler: User, PremiumPlan
# Başlangıç ve bitiş tarihleri
# Durum (active, expired, cancelled)
# Ödeme yöntemi
# İşlem ID
```

---

## API İşlemi Akışı

### Dükkan Listeleme ve Filtreleme

**İstek:**
```http
GET /api/workshops/?category=1&district=Adıyaman&min_rating=3&search=elektrik
```

**Yanıt:**
```json
{
  "count": 10,
  "results": [
    {
      "id": 1,
      "name": "ABC Elektrik",
      "category_name": "Elektrik",
      "district": "Adıyaman",
      "average_rating": 4.5,
      "total_reviews": 12,
      "is_premium": true
    }
  ]
}
```

### Yorum Ekleme

**İstek:**
```http
POST /api/reviews/?workshop=1
Content-Type: application/json

{
  "rating": 5,
  "comment": "Çok memnun kaldım!"
}
```

**Yanıt:**
```json
{
  "id": 1,
  "user_name": "Ahmet",
  "rating": 5,
  "comment": "Çok memnun kaldım!",
  "created_at": "2024-01-15T10:30:00Z"
}
```

### İşletme Yanıt Verme

**İstek:**
```http
POST /api/reviews/1/reply/
Content-Type: application/json

{
  "comment": "Teşekkür ederiz!"
}
```

---

## Authentikasyon

### JWT Token Akışı

1. **Kullanıcı kaydolur/giriş yapar**
```javascript
const login = async (username, password) => {
  const response = await usersAPI.login(username, password);
  localStorage.setItem('access_token', response.data.access);
  return response.data;
};
```

2. **Token localStorage'de saklanır**
```javascript
localStorage.setItem('access_token', token);
```

3. **Her istek için Authorization header'a eklenir**
```javascript
api.interceptors.request.use((config) => {
  const token = localStorage.getItem('access_token');
  if (token) {
    config.headers.Authorization = `Bearer ${token}`;
  }
  return config;
});
```

4. **Token süresi dolunca refresh edilir**
```javascript
// Otomatik olarak 401 hatası alındığında
POST /api/users/token/refresh/
Content-Type: application/json

{
  "refresh": "refresh_token"
}
```

### Korumalı Sayfalar

```javascript
import { useAuth } from '../hooks';
import { useNavigate } from 'react-router-dom';

function ProtectedPage() {
  const { user, isLoading } = useAuth();
  const navigate = useNavigate();

  useEffect(() => {
    if (!isLoading && !user) {
      navigate('/login');
    }
  }, [user, isLoading]);

  return <div>{/* Sayfa içeriği */}</div>;
}
```

---

## 🔄 Ortak Kullanılan Kalıplar

### Form İşleme

```javascript
const [formData, setFormData] = useState({
  name: '',
  email: '',
});

const handleChange = (e) => {
  const { name, value } = e.target;
  setFormData(prev => ({ ...prev, [name]: value }));
};

const handleSubmit = async (e) => {
  e.preventDefault();
  try {
    await api.post('/endpoint/', formData);
    alert('Başarılı!');
  } catch (error) {
    console.error('Hata:', error);
  }
};
```

### Liste ve Filtreleme

```javascript
const [filters, setFilters] = useState({ search: '', category: '' });
const [items, setItems] = useState([]);

useEffect(() => {
  fetchData();
}, [filters]);

const fetchData = async () => {
  try {
    const response = await api.get('/endpoint/', { params: filters });
    setItems(response.data);
  } catch (error) {
    console.error('Hata:', error);
  }
};
```

---

## 📦 TailwindCSS Örnek Bileşenler

### Buton
```jsx
<button className="bg-orange-600 text-white px-4 py-2 rounded-lg hover:bg-orange-700 disabled:opacity-50">
  Gönder
</button>
```

### Form Input
```jsx
<input
  type="text"
  className="w-full px-4 py-2 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-orange-500"
  placeholder="Girin..."
/>
```

### Kart
```jsx
<div className="bg-white p-6 rounded-lg shadow hover:shadow-lg transition">
  <h3 className="font-bold text-lg mb-2">Başlık</h3>
  <p className="text-gray-600">İçerik</p>
</div>
```

### Grid
```jsx
<div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
  {/* İçerik */}
</div>
```

---

## 🧪 Test Senaryoları

### Kullanıcı Kayıt ve Giriş
1. Kayıt sayfasına git
2. Tüm bilgileri doldur
3. Kaydol butonuna tıkla
4. Giriş sayfasına yönlendir
5. Kullanıcı adı ve şifre ile giriş yap

### Dükkan İnceleme
1. Ana sayfada kategoriler görün
2. Dükkan listesine tıkla
3. Filtreler çalışıyor mu kontrol et
4. Dükkan detayına tıkla
5. Yorumlar, saatler, hizmetler görsün

### Yorum Yapma
1. Dükkan detaysında oturum aç
2. Puan seç
3. Yorum yaz
4. Gönder
5. Yorum listesinde görün

---

## 🚀 Performans İpuçları

1. **Lazy Loading**: Resimlere `loading="lazy"` ekleyin
2. **Pagination**: Büyük listeler için sayfalama ekleyin
3. **Caching**: Token ve kullanıcı bilgisini cache'leyin
4. **Debouncing**: Arama inputunda debouncing yapın
5. **Code Splitting**: React.lazy ile sayfa bölütlemesi

---

## 📋 Kontrol Listesi

- [ ] Backend modelleri oluşturdum
- [ ] Frontend sayfa ve bileşenlerini yaptım
- [ ] API endpoints'lerini test ettim
- [ ] Authentikasyon çalışıyor
- [ ] Filtreleme ve arama yapılıyor
- [ ] CORS ayarları doğru
- [ ] Error handling'i implement ettim
- [ ] Responsive tasarım kontrol ettim
- [ ] Admin panelinde veri girebildim
- [ ] Tüm senaryo testleri başarılı

---

**Hepsi hazır! Geliştirmeye başlayabilirsiniz! 🎉**
