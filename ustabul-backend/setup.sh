#!/bin/bash

# UstaBul Backend Kurulum Betiği

echo "UstaBul Backend Kurulumu Başlıyor..."

# Python virtual environment oluştur
python -m venv venv

# Ortam etkinleştir (Windows için)
# venv\Scripts\activate
# Ortam etkinleştir (Mac/Linux için)
# source venv/bin/activate

# Bağımlılıkları yükle
pip install -r requirements.txt

# Veritabanı oluştur
python manage.py makemigrations
python manage.py migrate

# Admin kullanıcısı oluştur (isteğe bağlı)
# python manage.py createsuperuser

echo "Kurulum tamamlandı!"
echo "Şu komutu çalıştırarak sunucuyu başlatın:"
echo "python manage.py runserver"
