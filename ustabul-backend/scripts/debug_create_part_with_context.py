import os
import django
import traceback
from types import SimpleNamespace
import sys

# Ensure project root is on sys.path
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if ROOT not in sys.path:
    sys.path.insert(0, ROOT)

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
django.setup()

from apps.users.models import CustomUser
from apps.inventory.serializers import PartCreateSerializer

user = CustomUser.objects.filter(username='apitest_user').first()
print('found user:', bool(user))

payload = {
    'name': 'Debug API Test Part',
    'code': 'DBG-001',
    'brand': 'DbgBrand',
    'quantity': 5,
    'min_stock': 1,
    'current_purchase_price': 10.5,
    'current_sale_price': 15.0
}

serializer = PartCreateSerializer(data=payload, context={'request': SimpleNamespace(user=user)})
print('is_valid before save:', serializer.is_valid())
print('errors before save:', serializer.errors)

if serializer.is_valid():
    try:
        part = serializer.save()
        print('created part id:', part.id)
    except Exception:
        print('EXCEPTION DURING SAVE:')
        traceback.print_exc()
else:
    print('serializer invalid, not attempting save')
