#!/usr/bin/env python
import os
import django
import json

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
django.setup()

from apps.users.models import CustomUser
from django.contrib.auth import authenticate

# Tüm kullanıcıları listele
users = CustomUser.objects.all()
print(f"Toplam kullanıcı: {users.count()}")
for user in users:
    print(f"  - {user.username} ({user.get_role_display()})")

# Admin kullanıcı test et
print("\n--- Login Test ---")
user = authenticate(username='admin', password='admin123')
if user:
    print(f"✓ Login başarılı: {user.username}")
    print(f"  ID: {user.id}")
    print(f"  Email: {user.email}")
    print(f"  Role: {user.role}")
else:
    print("✗ Login başarısız")
