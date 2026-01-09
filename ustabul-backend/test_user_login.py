#!/usr/bin/env python
import os
import django
import json

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
django.setup()

from apps.users.models import CustomUser
from django.contrib.auth import authenticate

# Test kullanıcı oluştur
print("=" * 50)
print("TEST KULLANICI OLUŞTURMA VE GİRİŞ")
print("=" * 50)

test_username = 'testuser'
test_email = 'test@test.com'
test_password = 'test123'
test_role = 'customer'

# Mevcut kullanıcıyı sil ve yeni oluştur
try:
    existing_user = CustomUser.objects.get(username=test_username)
    existing_user.delete()
    print(f"✓ Eski {test_username} silindi")
except CustomUser.DoesNotExist:
    pass

# Yeni kullanıcı oluştur
user = CustomUser.objects.create_user(
    username=test_username,
    email=test_email,
    password=test_password,
    role=test_role
)
print(f"\n✓ KULLANICI OLUŞTURULDU")
print(f"  Username: {user.username}")
print(f"  Email: {user.email}")
print(f"  Role: {user.get_role_display()}")

# Giriş test et
print(f"\n--- GİRİŞ TESTİ ---")
authenticated_user = authenticate(username=test_username, password=test_password)

if authenticated_user:
    print(f"✓ GİRİŞ BAŞARILI!")
    print(f"  ID: {authenticated_user.id}")
    print(f"  Username: {authenticated_user.username}")
    print(f"  Email: {authenticated_user.email}")
    print(f"  Role: {authenticated_user.get_role_display()}")
    print(f"\n💡 Frontend'de kullanabilirsin:")
    print(f"   Username: {test_username}")
    print(f"   Password: {test_password}")
else:
    print(f"✗ GİRİŞ BAŞARISIZ!")

# Tüm kullanıcıları listele
print(f"\n--- TÜM KULLANICILAR ---")
users = CustomUser.objects.all()
for u in users:
    print(f"  • {u.username} ({u.get_role_display()})")
