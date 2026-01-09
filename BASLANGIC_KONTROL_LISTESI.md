# 🎯 UstaBul Projesi - Başlangıç Kontrol Listesi

## ✅ Kurulum Öncesi Kontrol

- [ ] Python 3.8+ yüklü mü? `python --version`
- [ ] Node.js yüklü mü? `node --version`
- [ ] npm yüklü mü? `npm --version`
- [ ] Git yüklü mü? `git --version` (isteğe bağlı)
- [ ] Text editor (VS Code, PyCharm, vb.) var mı?

---

## 🚀 Başlangıç Talimatları (Sırasıyla)

### Adım 1: Klasöre Git
```bash
cd "c:\Users\mcht7\Desktop\TEZ AGENT"
```

### Adım 2: Backend Başlat
```bash
# Yeni Terminal 1 (Backend)
cd ustabul-backend

# Virtual environment
python -m venv venv
venv\Scripts\activate

# Bağımlılıkları yükle
pip install -r requirements.txt

# Veritabanı oluştur
python manage.py migrate

# Admin kullanıcı oluştur
python manage.py createsuperuser
# Username: admin
# Password: admin123

# Sunucuyu başlat
python manage.py runserver
```

✅ Backend: http://localhost:8000

### Adım 3: Frontend Başlat
```bash
# Yeni Terminal 2 (Frontend)
cd ustabul-frontend

# Bağımlılıkları yükle
npm install

# Sunucuyu başlat
npm start
```

✅ Frontend: http://localhost:3000

---

## 🧪 İlk Test

1. Frontend'i aç: http://localhost:3000
2. Admin panelini aç: http://localhost:8000/admin
3. Admin bilgileri:
   - Username: admin
   - Password: admin123

4. Admin panelinde Kategoriler ekle:
   - Workshops > Categories > Add Category
   - Örn: "Elektrik", "Tornacılık", "Kaynakçılık"

5. Frontend'de kategorileri görmeli

---

## 📖 Dokümantasyon

| Dosya | İçerik | Ne Zaman Okuyacaksın |
|-------|--------|----------------------|
| README.md | Proje hakkında genel bilgi | Hemen |
| HIZLI_BASLA.md | 5 dakika kurulum | Hemen |
| KURULUM_REHBERI.md | Detaylı kurulum adımları | Sorun olursa |
| GELİŞTİRME_REHBERİ.md | Yeni feature ekleme | Geliştirme sırasında |
| PROJE_ÖZETI.md | Teknik mimarisi | Derinlemesine bilgi için |
| TAMAMLANMA_RAPORU.md | Ne yapıldı, ne kalması gerek | Referans olarak |

---

## 🛠️ VS Code Ayarlamaları (İsteğe Bağlı)

### Extensions Yükle
```
Python (Microsoft)
Pylance (Microsoft)
Django (Batistof)
ES7+ React/Redux/React-Native snippets (dsznajder)
Tailwind CSS IntelliSense (bradlc)
REST Client (humao.rest-client)
```

### Debug Configuration
`.vscode/launch.json` oluştur:
```json
{
  "version": "0.2.0",
  "configurations": [
    {
      "name": "Django",
      "type": "python",
      "request": "launch",
      "program": "${workspaceFolder}/ustabul-backend/manage.py",
      "args": ["runserver"],
      "django": true
    }
  ]
}
```

---

## 🧠 Proje Yapısını Anla

### Backend
```
ustabul-backend/
├── config/          # Django ayarları
├── apps/            # 6 ayrı app
│   ├── users/       # Kullanıcı
│   ├── workshops/   # Dükkanlar
│   ├── reviews/     # Yorumlar
│   ├── messaging/   # Mesajlar
│   ├── inventory/   # Stok
│   └── payments/    # Ödeme
└── manage.py
```

**Her app'in yapısı:**
- `models.py` - Veritabanı modelleri
- `views.py` - API view'ları
- `serializers.py` - JSON dönüşümü
- `urls.py` - Rotalar
- `admin.py` - Admin paneli

### Frontend
```
ustabul-frontend/
├── public/          # Static files
├── src/
│   ├── pages/       # 6 sayfa
│   ├── components/  # Bileşenler
│   ├── api.js       # API çağrıları
│   ├── AuthContext.js # Kimlik doğrulama
│   └── App.js       # Root component
└── package.json
```

---

## 🎯 İlk 30 Dakikada Ne Yapabilirsin

**Dakika 0-5:** Backend kurulumu
```bash
cd ustabul-backend
python -m venv venv
venv\Scripts\activate
pip install -r requirements.txt
python manage.py migrate
python manage.py createsuperuser
```

**Dakika 5-10:** Backend sunucusu başlat
```bash
python manage.py runserver
```

**Dakika 10-20:** Frontend kurulumu (yeni terminal)
```bash
cd ustabul-frontend
npm install
npm start
```

**Dakika 20-30:** Test etme
- Admin paneline giriş
- Kategori ekle
- Frontend'de kategorileri gör
- Kaydol sayfasını test et

---

## 🧩 İlk Feature Ekleme (Test)

### 1. Backend'e yeni field ekle
```python
# ustabul-backend/apps/workshops/models.py
class Workshop(models.Model):
    # ... existing fields ...
    phone_verified = models.BooleanField(default=False)  # NEW
```

### 2. Migration yap
```bash
python manage.py makemigrations
python manage.py migrate
```

### 3. Serializer'ı güncelle
```python
# ustabul-backend/apps/workshops/serializers.py
class WorkshopDetailSerializer(serializers.ModelSerializer):
    class Meta:
        model = Workshop
        fields = [
            # ... existing fields ...
            'phone_verified',  # NEW
        ]
```

### 4. Admin panelinde göster
```python
# ustabul-backend/apps/workshops/admin.py
@admin.register(Workshop)
class WorkshopAdmin(admin.ModelAdmin):
    list_display = [..., 'phone_verified']  # ADD
```

### 5. Frontend'i güncelle
```javascript
// ustabul-frontend/src/pages/WorkshopDetailPage.js
// Eğer phone_verified varsa badge göster
{workshop.phone_verified && (
  <span className="bg-green-100 text-green-800 px-2 py-1 rounded">
    ✓ Telefon Doğrulandı
  </span>
)}
```

---

## 🐛 Yaygın Hatalar ve Çözümleri

### Python hatası: "ModuleNotFoundError"
```bash
# Çözüm:
pip install -r requirements.txt
```

### npm hatası: "ERR! code ERESOLVE"
```bash
# Çözüm:
npm install --legacy-peer-deps
```

### Port kullanımda hatası
```bash
# Backend: Port 8000 kullanımda
python manage.py runserver 8001

# Frontend: Port 3000 kullanımda
npm start -- --port 3001
```

### CORS hatası
```
Access to XMLHttpRequest at 'http://localhost:8000/api/workshops/' 
from origin 'http://localhost:3000' has been blocked by CORS policy
```
**Çözüm:** Backend'de CORS_ALLOWED_ORIGINS kontrol et

### Database hatası
```bash
# Veritabanını sıfırla
rm db.sqlite3
python manage.py migrate
python manage.py createsuperuser
```

---

## 📊 Proje İstatistikleri

```
Backend:
- 6 Django Apps
- 13 Models
- 30+ API Endpoints
- ~1500 Satır Code

Frontend:
- 6 Pages
- 1 Context
- 1 Hook
- ~800 Satır Code

Database:
- 13 Tables
- SQLite (dev)
- PostgreSQL Ready

Documentation:
- 7 Markdown Files
- ~5000 Satır Yazı
```

---

## 🎓 Öğrenme Rotası

### Gün 1: Kurulum ve Temel Bilgi
- [ ] Projeyi kur
- [ ] Admin panelini gez
- [ ] Frontend sayfalarını gez
- [ ] README.md oku

### Gün 2: Backend Öğren
- [ ] Django model yapısını anla
- [ ] Admin panel'de veri ekle
- [ ] API endpoints'lerini test et (Postman/curl)
- [ ] GELİŞTİRME_REHBERİ.md oku

### Gün 3: Frontend Öğren
- [ ] React component yapısını anla
- [ ] api.js dosyasını anla
- [ ] Bir sayfada değişiklik yap
- [ ] Browser DevTools kullan

### Gün 4-5: Yeni Feature Ekle
- [ ] Kendi feature'ını planlığında
- [ ] Backend'e ekle
- [ ] Frontend'i güncelle
- [ ] Test et

---

## 💾 Backup ve Version Control

### .gitignore (eğer git kullanırsan)
```
# Python
venv/
__pycache__/
*.pyc
db.sqlite3

# Node
node_modules/
.env

# IDE
.vscode/
.idea/

# OS
.DS_Store
Thumbs.db
```

### Yapılacak
```bash
# Git repo oluştur (isteğe bağlı)
git init
git add .
git commit -m "UstaBul project initial commit"
```

---

## ✨ Başarı Işaretleri

Eğer bunu gördüysen başarılı demektir:

✅ Backend sunucusu başladı (http://localhost:8000)  
✅ Frontend sayfası açıldı (http://localhost:3000)  
✅ Admin paneline giriş yapıldı  
✅ Kategoriler listesi frontend'de göründü  
✅ Kayıt ve Giriş formu çalıştı  

**Tebrik ederiz! UstaBul'u başarıyla kurdum! 🎉**

---

## 🆘 Yardım Almak

1. **Kurulum hatası**: KURULUM_REHBERI.md oku
2. **Geliştirme sorusu**: GELİŞTİRME_REHBERİ.md oku
3. **Teknik soru**: PROJE_ÖZETI.md bak
4. **API hatası**: API documentation'ı kontrol et
5. **Terminal hatası**: Error message'i dikkatle oku

---

**Hazırsan başla! Başarılar! 🚀**
