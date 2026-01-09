#!/usr/bin/env python
import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
django.setup()

from apps.workshops.models import Category, Workshop, WorkingHours
from apps.users.models import CustomUser
from datetime import time

print("=" * 60)
print("TEST VERISI OLUŞTURMA")
print("=" * 60)

# Admin kullanıcı al
admin = CustomUser.objects.get(username='admin')

# Kategoriler
categories = Category.objects.all()
if categories.count() == 0:
    print("✗ Kategoriler oluşturulamadı")
    exit()

print(f"\n✓ {categories.count()} kategori bulundu")

# 5 test dükkanı oluştur
test_shops = [
    {
        'name': 'Elektrik Hizmetleri',
        'category': categories.first(),
        'phone': '05551234567',
        'address': 'Adıyaman Merkez',
        'district': 'Merkez',
    },
    {
        'name': 'Tornacılık Ustası',
        'category': categories.filter(name='Tornacılık').first(),
        'phone': '05552345678',
        'address': 'Adıyaman İstiklal Cad.',
        'district': 'Merkez',
    },
    {
        'name': 'Profesyonel Kaynakçılık',
        'category': categories.filter(name='Kaynakçılık').first(),
        'phone': '05553456789',
        'address': 'Adıyaman Sanayi Bölgesi',
        'district': 'Merkez',
    },
    {
        'name': 'Boyacılık Hizmeti',
        'category': categories.filter(name='Boyacılık').first(),
        'phone': '05554567890',
        'address': 'Adıyaman Atatürk Cad.',
        'district': 'Merkez',
    },
    {
        'name': 'Ahşap İşleri',
        'category': categories.filter(name='Marangozluk').first(),
        'phone': '05555678901',
        'address': 'Adıyaman Cumhuriyet Cad.',
        'district': 'Merkez',
    },
]

print("\n--- Dükkan Oluşturma ---")
for shop_data in test_shops:
    if not Workshop.objects.filter(name=shop_data['name']).exists():
        shop = Workshop.objects.create(
            owner=admin,
            name=shop_data['name'],
            category=shop_data['category'],
            phone=shop_data['phone'],
            address=shop_data['address'],
            district=shop_data['district'],
            is_active=True,
            average_rating=4.5,
            total_reviews=5,
        )
        print(f"✓ {shop.name} oluşturuldu")
        
        # Çalışma saatleri ekle
        days = [
            (1, '08:00:00', '17:00:00'),  # Pazartesi
            (2, '08:00:00', '17:00:00'),  # Salı
            (3, '08:00:00', '17:00:00'),  # Çarşamba
            (4, '08:00:00', '17:00:00'),  # Perşembe
            (5, '08:00:00', '17:00:00'),  # Cuma
            (6, '09:00:00', '14:00:00'),  # Cumartesi
        ]
        
        for day_num, open_time, close_time in days:
            WorkingHours.objects.get_or_create(
                workshop=shop,
                day_of_week=day_num,
                defaults={
                    'opening_time': open_time,
                    'closing_time': close_time,
                    'is_closed': False,
                }
            )
    else:
        print(f"✗ {shop_data['name']} zaten var")

print("\n--- İstatistik ---")
total_shops = Workshop.objects.count()
print(f"Toplam Dükkan: {total_shops}")

print("\n✓ TEST VERİSİ OLUŞTURULDU!")
