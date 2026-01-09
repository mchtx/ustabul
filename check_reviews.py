#!/usr/bin/env python
import os
import sys
import django

# Setup Django
sys.path.insert(0, r'c:\Users\mcht7\Desktop\TEZ AGENT\ustabul-backend')
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
django.setup()

from apps.reviews.models import Review

print("=== REVIEWS IN DATABASE ===")
reviews = Review.objects.all()
print(f"Total reviews: {reviews.count()}")
for review in reviews.order_by('-created_at')[:5]:
    print(f"- {review.user.username} (#{review.id}): {review.comment[:50]}... | Workshop: {review.workshop.name}")
