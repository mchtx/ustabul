# 🚀 UstaBul - Hızlı Başlangıç (5 Dakika)

## ⚡ Adım 1: Backend Başlat (Terminal 1)

```bash
cd ustabul-backend
python -m venv venv

# Windows
venv\Scripts\activate

# Mac/Linux
source venv/bin/activate

pip install -r requirements.txt
python manage.py migrate
python manage.py runserver
```

✅ Backend çalışıyor: http://localhost:8000

---

## ⚡ Adım 2: Frontend Başlat (Terminal 2)

```bash
cd ustabul-frontend
npm install
npm start
```

✅ Frontend çalışıyor: http://localhost:3000

---

## ⚡ Adım 3: Admin Paneline Gidin

1. Admin oluştur (Backend Terminal'de):
```bash
python manage.py createsuperuser
# Username: admin
# Password: admin123
```

2. Admin paneline git: http://localhost:8000/admin

3. Kategoriler ekle:
   - Workshops > Categories > Yeni Kategori
   - Örn: "Elektrik", "Tornacılık", "Kaynakçılık"

---

## 🧪 Test Edin

1. Frontend ana sayfaya git: http://localhost:3000
2. Kategoriler görünüyor mu?
3. "Kaydol" butonuna tıkla
4. Form doldur
5. Giriş yap
6. Profil sayfasını gör

---

## 📁 Proje Dosyaları

```
📦 TEZ AGENT
 ├── 📄 README.md                    ← Ana Dosya
 ├── 📄 KURULUM_REHBERI.md          ← Detaylı Kurulum
 ├── 📄 GELİŞTİRME_REHBERİ.md       ← Geliştirme Kılavuzu
 ├── 📄 PROJE_ÖZETI.md              ← Teknik Detaylar
 ├── 📄 HIZLI_BASLA.md              ← Bu dosya
 │
 ├── 🔷 ustabul-backend/
 │   ├── config/                    ← Django Config
 │   ├── apps/
 │   │   ├── users/                ← Kullanıcı Yönetimi
 │   │   ├── workshops/            ← Dükkan Yönetimi
 │   │   ├── reviews/              ← Yorum Sistemi
 │   │   ├── messaging/            ← Mesajlaşma
 │   │   ├── inventory/            ← Stok Yönetimi
 │   │   └── payments/             ← Premium Planlar
 │   ├── manage.py
 │   └── requirements.txt
 │
 └── 🔶 ustabul-frontend/
     ├── src/
     │   ├── pages/                ← 6 Sayfa
     │   ├── api.js                ← API Çağrıları
     │   ├── AuthContext.js        ← Kimlik Doğrulama
     │   └── App.js
     ├── package.json
     └── tailwind.config.js
```

---

## 🎯 Ana Sayfalar

| Sayfa | URL | Açıklama |
|-------|-----|----------|
| Ana Sayfa | `/` | Kategoriler, premium dükkanlar |
| Dükkan Listesi | `/workshops` | Arama ve filtreleme |
| Dükkan Detayı | `/workshops/1` | Bilgi, yorumlar, sohbet |
| Kaydol | `/register` | Yeni hesap |
| Giriş | `/login` | Var olan hesapla giriş |
| Profil | `/profile` | Kullanıcı bilgileri |

---

## 📡 API Örnekleri

### Dükkan Listesi
```bash
curl http://localhost:8000/api/workshops/
```

### Kategoriler
```bash
curl http://localhost:8000/api/workshops/categories/
```

### Giriş
```bash
curl -X POST http://localhost:8000/api/users/token/ \
  -H "Content-Type: application/json" \
  -d '{"username":"admin","password":"admin123"}'
```

---

## 🆘 Hata Giderme

| Problem | Çözüm |
|---------|-------|
| ModuleNotFoundError | `pip install -r requirements.txt` |
| npm ERR! | `npm install` tekrar çalıştır |
| Port 8000 kullanımda | `python manage.py runserver 8001` |
| Port 3000 kullanımda | `npm start -- --port 3001` |
| Database hatası | `rm db.sqlite3` ve `python manage.py migrate` |

---

## ✨ Başarı İşaretleri

✅ Backend sunucusu başladı  
✅ Frontend sunucusu başladı  
✅ http://localhost:3000 açılıyor  
✅ Admin paneline giriş yapılabildi  
✅ Kategoriler eklendi  
✅ Yeni kullanıcı kaydı yapıldı  
✅ Giriş yapıldı  
✅ Profil sayfası görüntülendi  

---

## 🎓 Sonraki Adımlar

1. **Admin Paneli Gez** (10 dakika)
   - Kategoriler ekle
   - Dükkân oluştur
   - Hizmet ve çalışma saatleri ayarla

2. **Frontend'i Öğren** (30 dakika)
   - Ana sayfayı incele
   - Dükkan arama yap
   - Yorum yaz

3. **Backend'i Öğren** (1 saat)
   - Django models'i anla
   - API endpoints'lerini test et
   - Admin panelini kustomize et

4. **Kendi Özelliklerini Ekle**
   - GELİŞTİRME_REHBERİ.md'yi oku
   - Yeni model oluştur
   - API endpoint ekle

---

## 📚 Kaynaklar

- **Django Docs**: https://docs.djangoproject.com
- **Django REST Framework**: https://www.django-rest-framework.org
- **React Docs**: https://react.dev
- **TailwindCSS**: https://tailwindcss.com

---

## 🆘 Sorun mu Var?

1. Terminal çıktısını dikkatli oku
2. Error message'i Google'da ara
3. KURULUM_REHBERI.md'yi kontrol et
4. GELİŞTİRME_REHBERİ.md'yi oku

---

**Hazırsan başla! 🎉 İlk hata alınca KURULUM_REHBERI.md'yi oku.**
