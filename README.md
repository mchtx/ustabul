# 🚀 UstaBul - Adıyaman Usta/Servis Bulma Platformu

**Adıyaman sanayi sektöründe güvenilir usta/servis bulma ve işletmeleri dijitalleştirme platformu.**

> ⚡ **Hızlı Başla**: `HIZLI_BASLA.md` dosyasını oku (5 dakika)  
> 📖 **Detaylı Kurulum**: `KURULUM_REHBERI.md` dosyasını oku  
> 🛠️ **Geliştirme**: `GELİŞTİRME_REHBERİ.md` dosyasını oku  
> 📊 **Proje Özeti**: `PROJE_ÖZETI.md` dosyasını oku

## Proje Mimarisi

### Backend (Django REST Framework)
- **Port**: 8000
- **URL**: http://localhost:8000
- **Admin Panel**: http://localhost:8000/admin

### Frontend (React)
- **Port**: 3000
- **URL**: http://localhost:3000

## Kurulum

### Backend Kurulumu

1. **Virtual Environment oluşturma**
```bash
cd ustabul-backend
python -m venv venv
# Windows
venv\Scripts\activate
# Mac/Linux
source venv/bin/activate
```

2. **Bağımlılıkları yükleme**
```bash
pip install -r requirements.txt
```

3. **Veritabanı oluşturma**
```bash
python manage.py makemigrations
python manage.py migrate
```

4. **Admin kullanıcısı oluşturma**
```bash
python manage.py createsuperuser
```

5. **Server başlatma**
```bash
python manage.py runserver
```

### Frontend Kurulumu

1. **Node.js bağımlılıklarını yükleme**
```bash
cd ustabul-frontend
npm install
```

2. **Server başlatma**
```bash
npm start
```

## Proje Yapısı

```
ustabul-backend/
├── config/              # Django ayarları
├── apps/
│   ├── users/          # Kullanıcı yönetimi
│   ├── workshops/      # Dükkan yönetimi
│   ├── reviews/        # Yorum sistemi
│   ├── messaging/      # Mesajlaşma
│   ├── inventory/      # Stok yönetimi
│   └── payments/       # Ödeme sistemi
├── manage.py
└── requirements.txt

ustabul-frontend/
├── public/
├── src/
│   ├── pages/          # Sayfalar
│   ├── components/     # Bileşenler
│   ├── api.js          # API istekleri
│   ├── AuthContext.js  # Kimlik doğrulama
│   ├── App.js
│   └── index.js
├── package.json
└── tailwind.config.js
```

## Temel Özellikler

### Müşteriler
- ✓ Kaydolmadan dükkânları gezebilme
- ✓ Kategori ve ilçe filtresi
- ✓ Puan ve yorum yazma
- ✓ Favorilere ekleme
- ✓ WhatsApp/Telefon ile iletişim
- ✓ Site içi mesajlaşma

### Dükkân Sahipleri
- ✓ Profil yönetimi
- ✓ Çalışma saatleri belirleme
- ✓ Hizmet ve fiyat yönetimi
- ✓ Yorum yanıtlama
- ✓ Müşteri mesajlarını yönetme
- ✓ (Opsiyonel) Stok yönetimi

### Parçacılar
- ✓ Ürün ekleme/düzenleme
- ✓ Stok takibi
- ✓ Düşük stok uyarıları
- ✓ Stok hareketleri

### Admin
- ✓ Dükkân yönetimi
- ✓ Kategori yönetimi
- ✓ Premium üyelik kontrolü
- ✓ Yorum moderasyonu
- ✓ Kullanıcı banlama

## API Endpoints

### Users
- `POST /api/users/register/` - Kayıt
- `POST /api/users/token/` - Giriş
- `GET /api/users/me/` - Profil
- `POST /api/users/change_password/` - Şifre değiştirme

### Workshops
- `GET /api/workshops/` - Dükkan listesi
- `GET /api/workshops/{id}/` - Dükkan detayı
- `GET /api/workshops/categories/` - Kategoriler
- `GET /api/workshops/my_workshops/` - Kendi dükkanlarım

### Reviews
- `GET /api/reviews/` - Yorum listesi
- `POST /api/reviews/` - Yorum oluşturma
- `POST /api/reviews/{id}/reply/` - Yanıt yazma

### Messaging
- `GET /api/messaging/conversations/` - Sohbetler
- `POST /api/messaging/conversations/start_conversation/` - Sohbet başlatma
- `POST /api/messaging/conversations/{id}/send_message/` - Mesaj gönderme

### Inventory
- `GET /api/inventory/products/` - Ürün listesi
- `POST /api/inventory/products/` - Ürün oluşturma
- `GET /api/inventory/products/low_stock/` - Düşük stok ürünleri

### Payments
- `GET /api/payments/plans/` - Premium planları
- `POST /api/payments/subscriptions/subscribe/` - Abone olma
- `GET /api/payments/subscriptions/` - Aboneliklerim

## Veritabanı Modelleri

### Users
- CustomUser (Özel kullanıcı)
- Favorite (Favori dükkanlar)

### Workshops
- Category (Kategoriler)
- Workshop (Dükkanlar)
- WorkingHours (Çalışma saatleri)
- Service (Hizmetler)

### Reviews
- Review (Yorum ve puanlama)
- ReviewReply (İşletme yanıtları)

### Messaging
- Conversation (Sohbetler)
- Message (Mesajlar)

### Inventory
- Product (Ürünler)
- StockMovement (Stok hareketleri)

### Payments
- PremiumPlan (Premium planları)
- Subscription (Abonelikler)
- Invoice (Faturalar)

## Teknolojiler

### Backend
- Django 4.2
- Django REST Framework 3.14
- Django CORS Headers 4.3
- SimpleJWT
- SQLite (geliştirme)

### Frontend
- React 18.2
- React Router 6.20
- Axios 1.6
- TailwindCSS 3.3

## Gelecek Özellikler

- [ ] Gerçek ödeme altyapısı (Iyzico/Stripe)
- [ ] Kampanya/reklam modülü
- [ ] İleri admin istatistikleri
- [ ] Diğer şehirlere genişleme
- [ ] Mobil uygulama

## Kontribüsyon

UstaBul projesine katkıda bulunmak için pull request gönderin.

## Lisans

Bu proje MIT lisansı altında sunulmaktadır.

---

**Not**: Adıyaman sanayi sektörüne dijital dönüşüm sağlamak için geliştirilen proje.
