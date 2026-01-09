#!/usr/bin/env python
import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
django.setup()

from apps.users.models import CustomUser

# Test kullanıcıları oluştur
users = [
    {'username': 'ali_musteri', 'email': 'ali@test.com', 'password': 'test123', 'first_name': 'Ali', 'last_name': 'Veli', 'role': 'customer'},
    {'username': 'mehmet_dukkan', 'email': 'mehmet@test.com', 'password': 'test123', 'first_name': 'Mehmet', 'last_name': 'Usta', 'role': 'workshop'},
    {'username': 'ayse_parcaci', 'email': 'ayse@test.com', 'password': 'test123', 'first_name': 'Ayşe', 'last_name': 'Parça', 'role': 'parts_dealer'},
]

for user_data in users:
    password = user_data.pop('password')
    user = CustomUser.objects.create_user(**user_data)
    user.set_password(password)
    user.save()
    print(f"✓ {user.username} ({user.get_role_display()}) oluşturuldu")
