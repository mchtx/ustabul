import requests

BASE = 'http://127.0.0.1:8000/api'

session = requests.Session()

# 1) Register (ignore if already exists)
reg_payload = {
    'username': 'apitest_user',
    'password': 'testpass123',
    'password_confirm': 'testpass123',
    'email': 'apitest@example.com',
    'role': 'parts_dealer'
}
print('Registering user (may fail if exists)...')
resp = session.post(f'{BASE}/users/register/', json=reg_payload)
print('register status', resp.status_code)

# 2) Login
login_payload = {'username': 'apitest_user', 'password': 'testpass123'}
print('Logging in...')
resp = session.post(f'{BASE}/users/login/', json=login_payload)
print('login status', resp.status_code)

# 3) GET parts list to ensure CSRF cookie is set (and minimal noise)
print('GET /api/inventory/parts/ to fetch list and set CSRF...')
resp = session.get(f'{BASE}/inventory/parts/')
print('LIST STATUS:', resp.status_code)
print('LIST RESPONSE-TYPE:', resp.headers.get('Content-Type'))
csrf = session.cookies.get('csrftoken')
print('CSRF cookie:', csrf)
print('LIST RESPONSE (first 400 chars):')
print(resp.text[:400])

# 4) Create a part with minimal payload
payload = {
    'name': 'API Test Part',
    'code': 'API-001',
    'brand': 'TestBrand',
    'quantity': 5,
    'min_stock': 1,
    'current_purchase_price': 10.5,
    'current_sale_price': 15.0
}
headers = {}
if csrf:
    headers['X-CSRFToken'] = csrf

print('Creating part...')
resp = session.post(f'{BASE}/inventory/parts/', json=payload, headers=headers)
print('CREATE STATUS:', resp.status_code)
print('CREATE RESPONSE-TYPE:', resp.headers.get('Content-Type'))
try:
    print('CREATE RESPONSE JSON:', resp.json())
except Exception:
    print('CREATE RESPONSE TEXT (first 800 chars):')
    print(resp.text[:800])

print('session cookies:', session.cookies.get_dict())
