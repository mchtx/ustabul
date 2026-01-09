# UstaBul Projesi - Proje Özeti

## 📋 Proje Bilgileri

**Proje Adı:** UstaBul - Adıyaman Usta/Servis Bulma Platformu

**Amaç:** Adıyaman sanayi sektöründe güvenilir usta/servis seçimini dijitalleştirerek müşteriler, işletmeler ve parçacılar arasında köprü kurmak.

**Hedef Şehir:** Adıyaman ve ilçeleri

---

## 🎯 Temel Özellikler

### Müşteriler İçin
✅ Kategoriye ve ilçeye göre dükkan arama  
✅ Puan ve yorum sistemi ile güvenilir usta seçimi  
✅ WhatsApp/Telefon ile tek tık iletişim  
✅ Site içi mesajlaşma  
✅ Favori dükkanlar sistemi  

### Dükkân Sahipleri İçin
✅ Profil ve hizmet yönetimi  
✅ Çalışma saatleri belirleme  
✅ Müşteri yorumlarına yanıt verme  
✅ Müşteri mesajlarını yönetme  
✅ Premium üyelik ile daha fazla görünürlük  

### Parçacılar İçin
✅ Ürün/parça stok yönetimi  
✅ Düşük stok uyarıları  
✅ Tedarikçi takibi  

### Admin Panel
✅ Dükkân yönetimi  
✅ Kategori yönetimi  
✅ Premium üyelik kontrolü  
✅ Yorum moderasyonu  
✅ Kullanıcı banlama  

---

## 🏗️ Teknik Mimarisi

### Backend Stack
- **Framework**: Django 4.2
- **API**: Django REST Framework
- **Authentikasyon**: JWT (SimpleJWT)
- **Veritabanı**: SQLite (dev) / PostgreSQL (prod)
- **Diğer**: Django CORS, Django Filter

### Frontend Stack
- **Framework**: React 18.2
- **Routing**: React Router 6.20
- **HTTP**: Axios
- **Styling**: TailwindCSS 3.3
- **State Management**: React Context API

### API Tasarım
- REST architecture
- JSON request/response
- JWT token-based authentication
- Filtreleme ve arama özellikleri
- Sayfalama (Pagination)

---

## 📊 Veritabanı Şeması

### Users App
```
CustomUser (Kullanıcı)
├── username
├── email
├── role (customer, workshop, parts_dealer, admin)
├── is_premium
├── is_banned
└── Favorite (Favori dükkanlar)
```

### Workshops App
```
Category (Kategori)
├── name
├── description
└── icon

Workshop (Dükkan)
├── owner (CustomUser)
├── name
├── category
├── address, phone, whatsapp
├── working_hours
├── services
├── average_rating
├── total_reviews
├── is_premium
└── is_active

WorkingHours (Çalışma Saatleri)
├── workshop
├── day_of_week
├── opening_time
├── closing_time
└── is_closed

Service (Hizmetler)
├── workshop
├── name
├── description
└── price
```

### Reviews App
```
Review (Yorum)
├── user
├── workshop
├── rating (1-5)
├── comment
├── is_verified
├── is_approved
└── ReviewReply (Yanıt)
    ├── workshop_owner
    ├── comment
    └── timestamp
```

### Messaging App
```
Conversation (Sohbet)
├── customer (CustomUser)
├── workshop
├── is_active
└── Message (Mesaj)
    ├── sender
    ├── content
    ├── is_read
    └── created_at
```

### Inventory App
```
Product (Ürün)
├── workshop
├── name, code
├── quantity
├── unit
├── price, cost
├── min_stock
├── supplier
├── image
└── StockMovement (Hareket)
    ├── product
    ├── movement_type (in, out, adjustment)
    ├── quantity
    ├── note
    └── created_by
```

### Payments App
```
PremiumPlan (Plan)
├── name
├── duration_days
├── price
├── features
└── Subscription (Abonelik)
    ├── user
    ├── plan
    ├── start_date
    ├── end_date
    ├── status
    ├── payment_method
    └── transaction_id

Invoice (Fatura)
├── subscription
├── invoice_number
├── amount
├── status (paid, pending, cancelled)
└── due_date
```

---

## 🔌 API Endpoints

### Authentication (Users)
```
POST   /api/users/register/              Yeni kullanıcı kaydı
POST   /api/users/token/                 Giriş (Token al)
POST   /api/users/token/refresh/         Token yenile
GET    /api/users/me/                    Profil bilgisi
POST   /api/users/change_password/       Şifre değiştir
```

### Workshops
```
GET    /api/workshops/                   Dükkan listesi (filtreleme ile)
GET    /api/workshops/{id}/              Dükkan detayı
POST   /api/workshops/                   Dükkan oluştur (dükkân sahibi)
PATCH  /api/workshops/{id}/              Dükkan güncelle
DELETE /api/workshops/{id}/              Dükkan sil (admin)
GET    /api/workshops/my_workshops/      Kendi dükkanlarım
GET    /api/workshops/categories/        Kategori listesi
```

### Reviews
```
GET    /api/reviews/?workshop={id}       Yorum listesi
POST   /api/reviews/?workshop={id}       Yorum oluştur
PATCH  /api/reviews/{id}/                Yorum güncelle
DELETE /api/reviews/{id}/                Yorum sil
POST   /api/reviews/{id}/reply/          İşletme yanıtı
```

### Messaging
```
GET    /api/messaging/conversations/     Sohbetler
GET    /api/messaging/conversations/{id}/ Sohbet detayı
POST   /api/messaging/conversations/start_conversation/  Sohbet başlat
POST   /api/messaging/conversations/{id}/send_message/   Mesaj gönder
POST   /api/messaging/conversations/{id}/mark_as_read/   Okundu işaretle
```

### Favorites
```
GET    /api/users/favorites/             Favoritiler
POST   /api/users/favorites/             Favoriye ekle
DELETE /api/users/favorites/{id}/        Favoriyden çıkar
```

### Inventory (Parçacılar)
```
GET    /api/inventory/products/          Ürün listesi
POST   /api/inventory/products/          Ürün oluştur
PATCH  /api/inventory/products/{id}/     Ürün güncelle
GET    /api/inventory/products/low_stock/ Düşük stok ürünleri
POST   /api/inventory/movements/         Stok hareketi kayıt
```

### Payments
```
GET    /api/payments/plans/              Premium planları
GET    /api/payments/subscriptions/      Abonelikler
POST   /api/payments/subscriptions/subscribe/  Abone ol
POST   /api/payments/subscriptions/{id}/cancel/ İptal et
GET    /api/payments/invoices/           Faturalar
```

---

## 📱 Frontend Sayfaları

| Sayfa | Route | Açıklama |
|-------|-------|----------|
| Ana Sayfa | `/` | Kategoriler, premium dükkanlar, CTA |
| Dükkan Listesi | `/workshops` | Filtreleme ve arama ile dükkan listesi |
| Dükkan Detayı | `/workshops/:id` | Tüm bilgiler, yorumlar, hizmetler |
| Giriş | `/login` | Kullanıcı giriş formu |
| Kayıt | `/register` | Yeni hesap oluşturma |
| Profil | `/profile` | Kullanıcı profili ve çıkış |

---

## 🔒 Güvenlik Özellikleri

✅ JWT token-based authentication  
✅ CORS koruması  
✅ Şifre hashlanması (Django built-in)  
✅ Yorum moderasyonu (is_approved)  
✅ Kullanıcı banlama sistemi  
✅ Admin-only endpoints  
✅ Ownership kontrolü (kendi dükkanını sadece sahibi düzenleyebilir)  

---

## 🚀 Deployment Hazırlığı

### Backend
```bash
# Production settings
DEBUG = False
ALLOWED_HOSTS = ['yourdomain.com']
DATABASES = PostgreSQL
SECRET_KEY = generate-strong-key

# Gunicorn + Nginx
gunicorn config.wsgi:application --bind 0.0.0.0:8000
```

### Frontend
```bash
# Build
npm run build

# Deployment (Vercel, Netlify, etc.)
npm run build
# .env.production
REACT_APP_API_URL=https://api.yourdomain.com
```

### Database Migration
```bash
# SQLite → PostgreSQL
python manage.py dumpdata > data.json
# PostgreSQL settings'e geç
python manage.py migrate
python manage.py loaddata data.json
```

---

## 📈 İstatistikler

| Bileşen | Sayı |
|---------|------|
| Django Apps | 6 |
| Models | 13 |
| API Endpoints | 30+ |
| React Pages | 6 |
| TailwindCSS Components | 10+ |
| Database Tables | 13 |

---

## 🎯 Gelecek Geliştirmeler

**Kısa Vadede:**
- [ ] Reel zamanlı mesajlaşma (WebSocket)
- [ ] Harita entegrasyonu (Google Maps)
- [ ] Gelişmiş admin dashboard'u
- [ ] Kampanya/reklam modülü

**Orta Vadede:**
- [ ] Gerçek ödeme altyapısı (Iyzico/Stripe)
- [ ] İleri istatistik paneli
- [ ] Bildirim sistemi
- [ ] Email notifications

**Uzun Vadede:**
- [ ] Mobil uygulama (React Native)
- [ ] Diğer şehirlere genişleme
- [ ] AI-powered öneriler
- [ ] Usta sertifikasyonu sistemi

---

## 📞 İletişim ve Destek

- **Backend Soruları**: Django & DRF dokumentasyon
- **Frontend Soruları**: React & TailwindCSS dokumentasyon
- **API Testing**: Postman / Thunder Client
- **Admin Panel**: http://localhost:8000/admin

---

## 📄 Dosya Yapısı

```
TEZ AGENT/
├── README.md                    # Ana dosya
├── KURULUM_REHBERI.md          # Kurulum talimatları
├── GELİŞTİRME_REHBERİ.md       # Geliştirme rehberi
├── PROJE_ÖZETI.md              # Bu dosya
│
├── ustabul-backend/
│   ├── config/
│   ├── apps/
│   ├── manage.py
│   ├── requirements.txt
│   └── .env.example
│
└── ustabul-frontend/
    ├── public/
    ├── src/
    ├── package.json
    ├── tailwind.config.js
    └── .env.example
```

---

## ✅ Başarı Kriterleri

- [x] Backend tüm modelleri içeriyor
- [x] Frontend tüm temel sayfaları içeriyor
- [x] API endpoints çalışıyor
- [x] Authentikasyon sistemi var
- [x] Filtreleme ve arama yapılıyor
- [x] Admin paneli var
- [x] TailwindCSS responsive tasarım
- [x] Türkçe içerik

---

**UstaBul Projesi Hazır! 🚀**

Kurulum için: `KURULUM_REHBERI.md`  
Geliştirme için: `GELİŞTİRME_REHBERİ.md`  
Ana bilgi için: `README.md`
