from django.contrib.auth.models import AbstractUser
from django.db import models


class CustomUser(AbstractUser):
    """Özel kullanıcı modeli"""
    
    ROLE_CHOICES = [
        ('customer', 'Müşteri'),
        ('workshop', 'Dükkân Sahibi'),
        ('parts_dealer', 'Parçacı'),
        ('admin', 'Admin'),
    ]
    
    role = models.CharField(
        max_length=20,
        choices=ROLE_CHOICES,
        default='customer',
        verbose_name='Rol'
    )
    phone = models.CharField(
        max_length=20,
        blank=True,
        verbose_name='Telefon'
    )
    profile_picture = models.ImageField(
        upload_to='profile_pictures/',
        blank=True,
        null=True,
        verbose_name='Profil Resmi'
    )
    is_premium = models.BooleanField(
        default=False,
        verbose_name='Premium Üye'
    )
    
    SUBSCRIPTION_CHOICES = [
        ('free', 'Ücretsiz'),
        ('premium', 'Premium'),
        ('premium_pro', 'Premium Pro'),
    ]
    
    subscription_level = models.CharField(
        max_length=20,
        choices=SUBSCRIPTION_CHOICES,
        default='free',
        verbose_name='Abonelik Seviyesi'
    )
    
    is_banned = models.BooleanField(
        default=False,
        verbose_name='Yasaklı'
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
        verbose_name = 'Kullanıcı'
        verbose_name_plural = 'Kullanıcılar'
        ordering = ['-created_at']
    
    def __str__(self):
        return f"{self.username} ({self.get_role_display()})"


class Favorite(models.Model):
    """Kullanıcı favori dükkanları"""
    user = models.ForeignKey(
        CustomUser,
        on_delete=models.CASCADE,
        related_name='favorites',
        verbose_name='Kullanıcı'
    )
    workshop = models.ForeignKey(
        'workshops.Workshop',
        on_delete=models.CASCADE,
        related_name='favorited_by',
        verbose_name='Dükkân'
    )
    created_at = models.DateTimeField(
        auto_now_add=True,
        verbose_name='Oluşturulma Tarihi'
    )
    
    class Meta:
        unique_together = ('user', 'workshop')
        verbose_name = 'Favori'
        verbose_name_plural = 'Favoriler'
    
    def __str__(self):
        return f"{self.user.username} - {self.workshop.name}"
