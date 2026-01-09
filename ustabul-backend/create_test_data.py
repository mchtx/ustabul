#!/usr/bin/env python
import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
django.setup()

from apps.workshops.models import Category, Workshop
from apps.users.models import CustomUser

# Kategoriler oluştur
categories_data = [
    'Elektrik',
    'Tornacılık',
    'Kaynakçılık',
    'Boyacılık',
    'Marangozluk',
]

print("--- Kategoriler ---")
for name in categories_data:
    if not Category.objects.filter(name=name).exists():
        Category.objects.create(name=name)
        print(f"✓ {name} kategorisi oluşturuldu")
    else:
        print(f"✗ {name} zaten var")

# Test dükkanı oluştur
print("\n--- Test Dükkanı ---")
workshop_user = CustomUser.objects.filter(role='workshop').first()
if not workshop_user:
    workshop_user = CustomUser.objects.create_user(
        username='dostum_elektrik',
        email='dostum@elektrik.com',
        password='test123',
        role='workshop',
        first_name='Dostum',
        last_name='Elektrikçi'
    )
    print(f"✓ Dükkân sahibi kullanıcısı oluşturuldu: {workshop_user.username}")

# Dükkan oluştur
if not Workshop.objects.filter(name='Dostum Elektrik').exists():
    category = Category.objects.first()
    workshop = Workshop.objects.create(
        name='Dostum Elektrik',
        owner=workshop_user,
        category=category,
        phone='05551234567',
        address='Adıyaman, Merkez',
        district='Merkez',
        description='Profesyonel elektrik hizmetleri',
        average_rating=4.5,
        is_active=True,
    )
    print(f"✓ Dükkan oluşturuldu: {workshop.name}")
else:
    print(f"✗ Dükkan zaten var")

print("\n--- İstatistik ---")
print(f"Toplam Kategori: {Category.objects.count()}")
print(f"Toplam Dükkan: {Workshop.objects.count()}")
print(f"Toplam Kullanıcı: {CustomUser.objects.count()}")
