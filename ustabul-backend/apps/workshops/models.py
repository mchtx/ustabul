from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator


class Category(models.Model):
    """Dükkan kategorileri"""
    name = models.CharField(
        max_length=100,
        unique=True,
        verbose_name='Kategori Adı'
    )
    description = models.TextField(
        blank=True,
        verbose_name='Açıklama'
    )
    icon = models.CharField(
        max_length=50,
        blank=True,
        verbose_name='İkon'
    )
    created_at = models.DateTimeField(
        auto_now_add=True,
        verbose_name='Oluşturulma Tarihi'
    )
    
    class Meta:
        verbose_name = 'Kategori'
        verbose_name_plural = 'Kategoriler'
        ordering = ['name']
    
    def __str__(self):
        return self.name


class Workshop(models.Model):
    """Usta/Sanayi dükkanları"""
    owner = models.ForeignKey(
        'users.CustomUser',
        on_delete=models.CASCADE,
        related_name='workshops',
        verbose_name='Sahibi'
    )
    name = models.CharField(
        max_length=200,
        verbose_name='Dükkân Adı'
    )
    category = models.ForeignKey(
        Category,
        on_delete=models.SET_NULL,
        null=True,
        related_name='workshops',
        verbose_name='Kategori'
    )
    description = models.TextField(
        blank=True,
        verbose_name='Açıklama'
    )
    address = models.TextField(
        verbose_name='Adres'
    )
    phone = models.CharField(
        max_length=20,
        verbose_name='Telefon'
    )
    whatsapp = models.CharField(
        max_length=20,
        blank=True,
        verbose_name='WhatsApp'
    )
    email = models.EmailField(
        blank=True,
        verbose_name='E-posta'
    )
    latitude = models.FloatField(
        null=True,
        blank=True,
        verbose_name='Enlem'
    )
    longitude = models.FloatField(
        null=True,
        blank=True,
        verbose_name='Boylam'
    )
    city = models.CharField(
        max_length=50,
        default='Adıyaman',
        verbose_name='Şehir'
    )
    district = models.CharField(
        max_length=50,
        verbose_name='İlçe'
    )
    neighborhood = models.CharField(
        max_length=100,
        blank=True,
        verbose_name='Mahalle'
    )
    image = models.ImageField(
        upload_to='workshops/',
        null=True,
        blank=True,
        verbose_name='Resim'
    )
    average_rating = models.FloatField(
        default=0,
        validators=[MinValueValidator(0), MaxValueValidator(5)],
        verbose_name='Ortalama Puan'
    )
    total_reviews = models.IntegerField(
        default=0,
        verbose_name='Toplam Yorum'
    )
    is_active = models.BooleanField(
        default=True,
        verbose_name='Aktif'
    )
    is_premium = models.BooleanField(
        default=False,
        verbose_name='Premium'
    )
    premium_until = models.DateTimeField(
        null=True,
        blank=True,
        verbose_name='Premium Tarihi'
    )
    is_closed_today = models.BooleanField(
        default=False,
        verbose_name='Bugün Kapalı'
    )
    closed_today_reason = models.CharField(
        max_length=200,
        blank=True,
        verbose_name='Kapalı Olma Sebebi'
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
        verbose_name = 'Dükkân'
        verbose_name_plural = 'Dükkanlar'
        ordering = ['-is_premium', '-average_rating', '-created_at']
    
    def __str__(self):
        return self.name


class WorkingHours(models.Model):
    """Dükkân çalışma saatleri"""
    DAY_CHOICES = [
        (0, 'Pazartesi'),
        (1, 'Salı'),
        (2, 'Çarşamba'),
        (3, 'Perşembe'),
        (4, 'Cuma'),
        (5, 'Cumartesi'),
        (6, 'Pazar'),
    ]
    
    workshop = models.ForeignKey(
        Workshop,
        on_delete=models.CASCADE,
        related_name='working_hours',
        verbose_name='Dükkân'
    )
    day_of_week = models.IntegerField(
        choices=DAY_CHOICES,
        verbose_name='Gün'
    )
    opening_time = models.TimeField(
        verbose_name='Açılış Saati'
    )
    closing_time = models.TimeField(
        verbose_name='Kapanış Saati'
    )
    is_closed = models.BooleanField(
        default=False,
        verbose_name='Kapalı'
    )
    
    class Meta:
        unique_together = ('workshop', 'day_of_week')
        verbose_name = 'Çalışma Saati'
        verbose_name_plural = 'Çalışma Saatleri'
        ordering = ['day_of_week']
    
    def __str__(self):
        return f"{self.workshop.name} - {self.get_day_of_week_display()}"


class Service(models.Model):
    """Dükkânın sunduğu hizmetler"""
    workshop = models.ForeignKey(
        Workshop,
        on_delete=models.CASCADE,
        related_name='services',
        verbose_name='Dükkân'
    )
    name = models.CharField(
        max_length=200,
        verbose_name='Hizmet Adı'
    )
    description = models.TextField(
        blank=True,
        verbose_name='Açıklama'
    )
    price = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        null=True,
        blank=True,
        verbose_name='Fiyat'
    )
    
    class Meta:
        verbose_name = 'Hizmet'
        verbose_name_plural = 'Hizmetler'
    
    def __str__(self):
        return f"{self.workshop.name} - {self.name}"
