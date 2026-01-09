# UstaBul Projesi - Başlangıç Rehberi

## 🚀 Hızlı Başlangıç

### Gereksinimler
- Python 3.8+
- Node.js 14+
- npm veya yarn

---

## 1️⃣ BACKEND KURULUMU (Django)

### Adım 1: Backend klasörüne gidin
```bash
cd ustabul-backend
```

### Adım 2: Virtual Environment oluşturun

**Windows:**
```bash
python -m venv venv
venv\Scripts\activate
```

**Mac/Linux:**
```bash
python -m venv venv
source venv/bin/activate
```

### Adım 3: Bağımlılıkları yükleyin
```bash
pip install -r requirements.txt
```

### Adım 4: Veritabanını oluşturun
```bash
python manage.py makemigrations
python manage.py migrate
```

### Adım 5: Admin kullanıcısı oluşturun (İsteğe bağlı)
```bash
python manage.py createsuperuser
# Bilgileri doldurun:
# Username: admin
# Email: admin@example.com
# Password: admin123 (ya da seçtiğiniz şifre)
```

### Adım 6: Backend sunucusunu başlatın
```bash
python manage.py runserver
```

**Başarı!** Backend http://localhost:8000 adresinde çalışıyor.

Admin paneline erişmek için: http://localhost:8000/admin

---

## 2️⃣ FRONTEND KURULUMU (React)

### Adım 1: Frontend klasörüne gidin (yeni terminal açın)
```bash
cd ustabul-frontend
```

### Adım 2: Bağımlılıkları yükleyin
```bash
npm install
```

### Adım 3: Frontend sunucusunu başlatın
```bash
npm start
```

**Başarı!** Frontend http://localhost:3000 adresinde çalışıyor.

---

## 🧪 Test Etme

### 1. Ana sayfaya gidin
http://localhost:3000

### 2. Kayıt olun
- Rol seçin: Müşteri / Dükkân Sahibi / Parçacı
- Bilgileri doldurun ve kaydolun

### 3. Admin panelinde kategoriler ekleyin
- Admin paneline gidin: http://localhost:8000/admin
- Username: admin
- Password: admin123
- Dükkan > Kategori > Yeni Kategori ekleyin

### 4. Dükkanlar test edin
- Frontend ana sayfada kategorileri göreceksiniz
- Dükkanları gözatabileceksiniz

---

## 📁 Proje Yapısı

```
TEZ AGENT/
├── ustabul-backend/          # Django REST API
│   ├── config/
│   │   ├── settings.py       # Django ayarları
│   │   ├── urls.py
│   │   └── wsgi.py
│   ├── apps/
│   │   ├── users/            # Kullanıcı yönetimi
│   │   ├── workshops/        # Dükkan yönetimi
│   │   ├── reviews/          # Yorum sistemi
│   │   ├── messaging/        # Mesajlaşma
│   │   ├── inventory/        # Stok yönetimi
│   │   └── payments/         # Ödeme sistemi
│   ├── manage.py
│   ├── requirements.txt
│   └── db.sqlite3            # Veritabanı (oluşturulduktan sonra)
│
├── ustabul-frontend/         # React uygulaması
│   ├── public/
│   ├── src/
│   │   ├── pages/           # Sayfalar
│   │   ├── components/      # Bileşenler
│   │   ├── api.js           # API çağrıları
│   │   ├── AuthContext.js   # Kimlik doğrulama
│   │   ├── App.js
│   │   └── index.js
│   ├── package.json
│   └── tailwind.config.js
│
└── README.md
```

---

## 🔧 Konfigürasyon

### Backend Ortam Değişkenleri (.env)
```
SECRET_KEY=your-secret-key
DEBUG=True
ALLOWED_HOSTS=localhost,127.0.0.1
```

### Frontend Ortam Değişkenleri (.env)
```
REACT_APP_API_URL=http://localhost:8000/api
```

---

## 💾 Veritabanı

Proje SQLite kullanmaktadır. İlk çalıştırmada otomatik oluşturulur.

- **Dosya**: `ustabul-backend/db.sqlite3`

Veritabanını sıfırlamak için:
```bash
rm db.sqlite3
python manage.py makemigrations
python manage.py migrate
python manage.py createsuperuser
```

---

## 🌐 API Endpoints

### Kullanıcı İşlemleri
```
POST   /api/users/register/            - Kayıt
POST   /api/users/token/               - Giriş
GET    /api/users/me/                  - Profil
GET    /api/users/favorites/           - Favoritiler
```

### Dükkanlar
```
GET    /api/workshops/                 - Dükkan Listesi
GET    /api/workshops/{id}/            - Dükkan Detayı
GET    /api/workshops/categories/      - Kategoriler
GET    /api/workshops/my_workshops/    - Kendi Dükkanlarım
```

### Yorumlar
```
GET    /api/reviews/                   - Yorum Listesi
POST   /api/reviews/                   - Yorum Oluştur
POST   /api/reviews/{id}/reply/        - Yanıt Ver
```

### Mesajlaşma
```
GET    /api/messaging/conversations/   - Sohbetler
POST   /api/messaging/conversations/start_conversation/  - Sohbet Başlat
```

### Stok Yönetimi
```
GET    /api/inventory/products/        - Ürünler
POST   /api/inventory/products/        - Ürün Ekle
```

### Premium Planlar
```
GET    /api/payments/plans/            - Planlar
POST   /api/payments/subscriptions/subscribe/  - Abone Ol
```

---

## 🆘 Sorun Giderme

### Backend başlamıyor
```bash
# Veritabanını sıfırla
rm db.sqlite3
python manage.py migrate

# Bağlantı noktası (Port) kullanımda
# 8000 yerine başka bir port kullan
python manage.py runserver 8001
```

### Frontend bağlanmıyor
```bash
# Bağlantı noktası çakışması
# 3000 yerine başka bir port kullan
npm start -- --port 3001
```

### CORS hatası
- Backend settings.py dosyasında CORS_ALLOWED_ORIGINS kontrol edin
- Frontend URL'si listeye eklediğinden emin olun

---

## 📱 Frontend Sayfaları

- **Ana Sayfa** (`/`) - Kategoriler ve premium dükkanlar
- **Dükkan Listesi** (`/workshops`) - Filtreli liste
- **Dükkan Detayı** (`/workshops/:id`) - Bilgiler, yorumlar, hizmetler
- **Giriş** (`/login`) - Kimlik doğrulaması
- **Kayıt** (`/register`) - Yeni hesap oluşturma
- **Profil** (`/profile`) - Kendi profili

---

## 🎨 Tasarım

Proje **TailwindCSS** kullanarak responsive tasarım yapılmıştır.

Renk şeması:
- **Ana Renk**: Orange (#FF6B35)
- **Arka Plan**: Gray (#F3F4F6)

---

## 📝 Sonraki Adımlar

1. **Veri Girişi**
   - Admin panelinde kategoriler ekleyin
   - Test dükkanları oluşturun
   - Premium planları yapılandırın

2. **Geliştirme**
   - Admin dashbord'u oluşturun
   - Harita entegrasyonu ekleyin
   - Ödeme sistemini implemente edin
   - WebSocket ile gerçek zamanlı mesajlaşma

3. **Deployment**
   - Backend: Gunicorn + Nginx
   - Frontend: Vercel / Netlify
   - Database: PostgreSQL
   - Storage: AWS S3 / Google Cloud Storage

---

## 📞 Destek

Sorularınız için:
- Backend: Django belgelerine bakın
- Frontend: React belgelerine bakın
- API: Admin panelini kullanarak test edin

---

**Başarıyla kuruldu! UstaBul'a hoş geldiniz! 🎉**
