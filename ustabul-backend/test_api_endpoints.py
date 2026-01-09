#!/usr/bin/env python
import os
import django
import json
from io import StringIO
from django.test import Client

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
django.setup()

from apps.users.models import CustomUser
from django.contrib.auth import authenticate

print("=" * 60)
print("API ENDPOINT TEST")
print("=" * 60)

# Django test client'ını kullan
client = Client()

# Test 1: Login endpoint test
print("\n1️⃣  LOGIN ENDPOINT TEST")
print("-" * 60)
login_response = client.post('/api/users/login/', {
    'username': 'testuser',
    'password': 'test123'
}, content_type='application/json')

print(f"Status Code: {login_response.status_code}")
if login_response.status_code == 200:
    print(f"✓ Login başarılı!")
    print(f"Response: {login_response.json()}")
else:
    print(f"✗ Login başarısız")
    print(f"Response: {login_response.content.decode()}")

# Test 2: Register endpoint test
print("\n2️⃣  REGISTER ENDPOINT TEST")
print("-" * 60)
register_response = client.post('/api/users/register/', {
    'username': 'newuser123',
    'email': 'newuser@test.com',
    'password': 'newpass123',
    'password_confirm': 'newpass123',
    'role': 'customer',
    'first_name': 'Test',
    'last_name': 'User'
}, content_type='application/json')

print(f"Status Code: {register_response.status_code}")
if register_response.status_code in [200, 201]:
    print(f"✓ Register başarılı!")
    print(f"Response: {register_response.json()}")
else:
    print(f"✗ Register başarısız")
    print(f"Response: {register_response.content.decode()}")

# Test 3: Admin login test
print("\n3️⃣  ADMIN LOGIN TEST")
print("-" * 60)
admin_response = client.post('/api/users/login/', {
    'username': 'admin',
    'password': 'admin123'
}, content_type='application/json')

print(f"Status Code: {admin_response.status_code}")
if admin_response.status_code == 200:
    print(f"✓ Admin login başarılı!")
    print(f"Response: {admin_response.json()}")
else:
    print(f"✗ Admin login başarısız")
    print(f"Response: {admin_response.content.decode()}")

print("\n" + "=" * 60)
print("TEST TÜRKİ!")
print("=" * 60)
