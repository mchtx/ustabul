import os
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
import django
django.setup()
from apps.inventory.serializers import PartCreateSerializer

# Simulate payload similar to frontend
data = {
    'name': '',
    'code': '',
    'brand': '',
    'quantity': 0,
    'min_stock': 0,
    'current_purchase_price': 0,
    'current_sale_price': 0,
    # 'category': None
}

s = PartCreateSerializer(data=data)
print('is_valid=', s.is_valid())
print('errors=', s.errors)

# Also try with some mismatched fields to reproduce frontend payload
payload2 = {
    'name': '',
    'code': '',
    'brand': '',
    'quantity': 0,
    'min_stock_level': 0,  # old frontend field
    'unit_price': 0,       # old frontend field
}

s2 = PartCreateSerializer(data=payload2)
print('--- payload2 ---')
print('is_valid=', s2.is_valid())
print('errors=', s2.errors)
