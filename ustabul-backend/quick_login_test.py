#!/usr/bin/env python
import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
django.setup()

from django.test import Client
import json

client = Client()

# Test 1: Login endpoint test
print("=" * 60)
print("LOGIN ENDPOINT TEST")
print("=" * 60)

login_data = json.dumps({
    'username': 'admin',
    'password': 'admin123'
})

response = client.post(
    '/api/users/login/',
    data=login_data,
    content_type='application/json'
)

print(f"\nStatus Code: {response.status_code}")
print(f"Response: {response.json()}")

if response.status_code == 200:
    print("\n✓ LOGIN BAŞARILI!")
    print(f"  Gelen Veriler:")
    data = response.json()
    for key, value in data.items():
        print(f"    - {key}: {value}")
else:
    print("\n✗ LOGIN BAŞARISIZ!")
    print(f"  Hata: {response.content.decode()}")
