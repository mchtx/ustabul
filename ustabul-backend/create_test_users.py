#!/usr/bin/env python
import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
django.setup()

from apps.users.models import CustomUser

# Test kullanıcıları oluştur
test_users = [
    {'username': 'test_customer', 'email': 'customer@test.com', 'password': 'test123', 'role': 'customer'},
    {'username': 'test_workshop', 'email': 'workshop@test.com', 'password': 'test123', 'role': 'workshop'},
    {'username': 'test_dealer', 'email': 'dealer@test.com', 'password': 'test123', 'role': 'parts_dealer'},
]

for user_data in test_users:
    username = user_data['username']
    if not CustomUser.objects.filter(username=username).exists():
        CustomUser.objects.create_user(
            username=user_data['username'],
            email=user_data['email'],
            password=user_data['password'],
            role=user_data['role']
        )
        print(f"✓ {username} oluşturuldu!")
    else:
        print(f"✗ {username} zaten var.")
