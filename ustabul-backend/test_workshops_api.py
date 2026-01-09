#!/usr/bin/env python
import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
django.setup()

from django.test import Client
import json

client = Client()

# Test: Workshops list endpoint
print("=" * 60)
print("WORKSHOPS LIST ENDPOINT TEST")
print("=" * 60)

response = client.get('/api/workshops/')

print(f"\nStatus Code: {response.status_code}")
data = response.json()

if isinstance(data, list):
    print(f"\n✓ {len(data)} dükkan bulundu")
    for i, ws in enumerate(data[:3], 1):
        print(f"\n{i}. {ws.get('name', 'N/A')}")
        print(f"   - ID: {ws.get('id')}")
        print(f"   - Kategori: {ws.get('category_name', 'N/A')}")
        print(f"   - İlçe: {ws.get('district', 'N/A')}")
        print(f"   - Puan: {ws.get('average_rating')}")
        print(f"   - Yorum: {ws.get('total_reviews')}")
else:
    print(f"Response: {json.dumps(data, indent=2, ensure_ascii=False)}")

print("\n" + "=" * 60)
