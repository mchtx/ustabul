from django.db import models
from django.utils import timezone
from datetime import timedelta


class PremiumPlan(models.Model):
    """Premium planları"""
    name = models.CharField(
        max_length=100,
        unique=True,
        verbose_name='Plan Adı'
    )
    description = models.TextField(
        blank=True,
        verbose_name='Açıklama'
    )
    
    LEVEL_CHOICES = [
        ('premium', 'Premium'),
        ('premium_pro', 'Premium Pro'),
    ]
    
    level = models.CharField(
        max_length=20,
        choices=LEVEL_CHOICES,
        default='premium',
        verbose_name='Seviye'
    )
    
    duration_days = models.IntegerField(
        default=30,
        verbose_name='Süre (Gün)'
    )
    price = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        verbose_name='Fiyat'
    )
    features = models.TextField(
        blank=True,
        verbose_name='Özellikler'
    )
    is_active = models.BooleanField(
        default=True,
        verbose_name='Aktif'
    )
    created_at = models.DateTimeField(
        auto_now_add=True,
        verbose_name='Oluşturulma Tarihi'
    )
    
    class Meta:
        verbose_name = 'Premium Plan'
        verbose_name_plural = 'Premium Planlar'
        ordering = ['price']
    
    def __str__(self):
        return f"{self.name} - {self.price}₺"


class Subscription(models.Model):
    """Premium abonelik"""
    STATUS_CHOICES = [
        ('active', 'Aktif'),
        ('expired', 'Süresi Dolmuş'),
        ('cancelled', 'İptal Edildi'),
    ]
    
    user = models.ForeignKey(
        'users.CustomUser',
        on_delete=models.CASCADE,
        related_name='subscriptions',
        verbose_name='Kullanıcı'
    )
    plan = models.ForeignKey(
        PremiumPlan,
        on_delete=models.SET_NULL,
        null=True,
        related_name='subscriptions',
        verbose_name='Plan'
    )
    start_date = models.DateTimeField(
        auto_now_add=True,
        verbose_name='Başlangıç Tarihi'
    )
    end_date = models.DateTimeField(
        verbose_name='Bitiş Tarihi'
    )
    status = models.CharField(
        max_length=20,
        choices=STATUS_CHOICES,
        default='active',
        verbose_name='Durum'
    )
    payment_method = models.CharField(
        max_length=50,
        blank=True,
        verbose_name='Ödeme Yöntemi'
    )
    transaction_id = models.CharField(
        max_length=200,
        blank=True,
        unique=True,
        verbose_name='İşlem ID'
    )
    created_at = models.DateTimeField(
        auto_now_add=True,
        verbose_name='Oluşturulma Tarihi'
    )
    updated_at = models.DateTimeField(
        auto_now=True,
        verbose_name='Güncellenme Tarihi'
    )
    
    class Meta:
        verbose_name = 'Abonelik'
        verbose_name_plural = 'Abonelikler'
        ordering = ['-start_date']
    
    def __str__(self):
        return f"{self.user.username} - {self.plan.name}"
    
    def save(self, *args, **kwargs):
        if not self.end_date and self.plan:
            self.end_date = self.start_date + timedelta(days=self.plan.duration_days)
        
        # Durumu güncelle
        if self.end_date < timezone.now():
            self.status = 'expired'
        
        super().save(*args, **kwargs)
    
    @property
    def is_active(self):
        return self.status == 'active' and self.end_date > timezone.now()


class Invoice(models.Model):
    """Fatura"""
    subscription = models.ForeignKey(
        Subscription,
        on_delete=models.CASCADE,
        related_name='invoices',
        verbose_name='Abonelik'
    )
    invoice_number = models.CharField(
        max_length=50,
        unique=True,
        verbose_name='Fatura Numarası'
    )
    amount = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        verbose_name='Tutar'
    )
    status = models.CharField(
        max_length=20,
        choices=[
            ('paid', 'Ödendi'),
            ('pending', 'Beklemede'),
            ('cancelled', 'İptal Edildi'),
        ],
        default='pending',
        verbose_name='Durum'
    )
    issued_at = models.DateTimeField(
        auto_now_add=True,
        verbose_name='Düzenlenme Tarihi'
    )
    due_date = models.DateTimeField(
        verbose_name='Son Ödeme Tarihi'
    )
    paid_at = models.DateTimeField(
        null=True,
        blank=True,
        verbose_name='Ödeme Tarihi'
    )
    
    class Meta:
        verbose_name = 'Fatura'
        verbose_name_plural = 'Faturalar'
        ordering = ['-issued_at']
    
    def __str__(self):
        return f"{self.invoice_number} - {self.amount}₺"
