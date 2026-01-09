import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
django.setup()

from django.contrib.auth import authenticate
from apps.users.models import CustomUser

username = 'testuser'
password = 'Test123456'

print(f"Kullanıcı: {username}")
print(f"Şifre: {password}")

# Veritabanında kullanıcı olup olmadığını kontrol et
user = CustomUser.objects.filter(username=username).first()
if user:
    print(f"✓ Kullanıcı bulundu: {user.username}")
    print(f"✓ Şifre doğrulama: {user.check_password(password)}")
    print(f"✓ Kullanıcı aktif mi: {user.is_active}")
else:
    print("✗ Kullanıcı bulunamadı!")

# authenticate fonksiyonunu dene
auth_user = authenticate(username=username, password=password)
if auth_user:
    print(f"✓ Authenticate başarılı: {auth_user.username}")
else:
    print("✗ Authenticate başarısız!")
