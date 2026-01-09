#!/usr/bin/env python
import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
django.setup()

from apps.users.models import CustomUser

# Admin kullanıcı oluştur
if not CustomUser.objects.filter(username='admin').exists():
    CustomUser.objects.create_superuser('admin', 'admin@ustabul.local', 'admin123', role='admin')
    print("✓ Admin kullanıcısı başarıyla oluşturuldu!")
    print("  Username: admin")
    print("  Password: admin123")
else:
    print("✗ Admin kullanıcısı zaten var.")
