from django.db import models
from django.core.validators import MinValueValidator
from django.utils import timezone
import uuid


# ÖN TANIMLI KATEGORİLER
PART_CATEGORIES = [
    ('Motor', 'Motor'),
    ('Fren', 'Fren'),
    ('Elektrik', 'Elektrik'),
    ('Süspansiyon', 'Süspansiyon'),
    ('Debriyaj', 'Debriyaj'),
    ('Şanzıman', 'Şanzıman'),
    ('Kaporta', 'Kaporta'),
    ('Filtre', 'Filtre'),
    ('Yağ & Sarf', 'Yağ & Sarf'),
]

# FREN ALT KATEGORİLERİ
FREN_SUBCATEGORIES = [
    ('Balata', 'Balata'),
    ('Disk', 'Disk'),
    ('Merkez', 'Merkez'),
    ('Kampana', 'Kampana'),
    ('Fren Hattı', 'Fren Hattı'),
]

# MOTOR ALT KATEGORİLERİ
MOTOR_SUBCATEGORIES = [
    ('Piston', 'Piston'),
    ('Segman', 'Segman'),
    ('Krank', 'Krank'),
    ('Yatak', 'Yatak'),
    ('Subap', 'Subap'),
    ('Radyatör', 'Radyatör'),
    ('Termostat', 'Termostat'),
    ('Su Pompası', 'Su Pompası'),
]

# ELEKTRİK ALT KATEGORİLERİ
ELEKTRIK_SUBCATEGORIES = [
    ('Alternatör', 'Alternatör'),
    ('Marş Motoru', 'Marş Motoru'),
    ('Buji', 'Buji'),
    ('Bobine', 'Bobine'),
    ('Ampul', 'Ampul'),
    ('Sigorta', 'Sigorta'),
    ('Kablo', 'Kablo'),
]

# SÜSPANSİYON ALT KATEGORİLERİ
SUSPANSION_SUBCATEGORIES = [
    ('Amortisör', 'Amortisör'),
    ('Yay', 'Yay'),
    ('Rot', 'Rot'),
    ('Rotil', 'Rotil'),
    ('Burç', 'Burç'),
    ('Takoz', 'Takoz'),
]

# DEBRİYAJ ALT KATEGORİLERİ
DEBRIYAJ_SUBCATEGORIES = [
    ('Debriyaj Seti', 'Debriyaj Seti'),
    ('Debriyaj Balatası', 'Debriyaj Balatası'),
    ('Baskı', 'Baskı'),
    ('Rulman', 'Rulman'),
]

# ŞANZIMAN ALT KATEGORİLERİ
SANZIMAN_SUBCATEGORIES = [
    ('Vites Kutusu', 'Vites Kutusu'),
    ('Debriyaj Balatası', 'Debriyaj Balatası'),
    ('Yağ', 'Yağ'),
    ('Filtre', 'Filtre'),
]

# KAPORTA ALT KATEGORİLERİ
KAPORTA_SUBCATEGORIES = [
    ('Kapı', 'Kapı'),
    ('Çamurluk', 'Çamurluk'),
    ('Tampon', 'Tampon'),
    ('Kaput', 'Kaput'),
    ('Bagaj Kapağı', 'Bagaj Kapağı'),
    ('Ayna', 'Ayna'),
]

# FİLTRE ALT KATEGORİLERİ
FILTRE_SUBCATEGORIES = [
    ('Hava Filtresi', 'Hava Filtresi'),
    ('Yağ Filtresi', 'Yağ Filtresi'),
    ('Yakıt Filtresi', 'Yakıt Filtresi'),
    ('Kabin Filtresi', 'Kabin Filtresi'),
]

# YAĞ & SARF ALT KATEGORİLERİ
YAG_SARF_SUBCATEGORIES = [
    ('Motor Yağı', 'Motor Yağı'),
    ('Şanzıman Yağı', 'Şanzıman Yağı'),
    ('Fren Hidroliği', 'Fren Hidroliği'),
    ('Soğutma Sıvısı', 'Soğutma Sıvısı'),
    ('Cam Sileceği', 'Cam Sileceği'),
]


class Vehicle(models.Model):
    """Araç tanımı"""
    brand = models.CharField(max_length=100, verbose_name='Marka')
    model = models.CharField(max_length=100, verbose_name='Model')
    year_from = models.IntegerField(verbose_name='Başlangıç Yılı')
    year_to = models.IntegerField(null=True, blank=True, verbose_name='Bitiş Yılı')
    engine = models.CharField(max_length=100, blank=True, verbose_name='Motor')
    engine_code = models.CharField(max_length=50, blank=True, verbose_name='Motor Kodu')
    
    class Meta:
        verbose_name = 'Araç'
        verbose_name_plural = 'Araçlar'
        ordering = ['brand', 'model', 'year_from']
        unique_together = ['brand', 'model', 'year_from', 'year_to', 'engine']
    
    def __str__(self):
        year_str = f"{self.year_from}"
        if self.year_to:
            year_str += f"-{self.year_to}"
        engine_str = f" ({self.engine})" if self.engine else ""
        return f"{self.brand} {self.model} {year_str}{engine_str}"


class PartCategory(models.Model):
    """Parça kategorisi - ön tanımlı"""
    name = models.CharField(max_length=100, verbose_name='Kategori Adı')
    subcategory = models.CharField(max_length=100, blank=True, verbose_name='Alt Kategori')
    is_active = models.BooleanField(default=True, verbose_name='Aktif')
    
    class Meta:
        verbose_name = 'Parça Kategorisi'
        verbose_name_plural = 'Parça Kategorileri'
        ordering = ['name', 'subcategory']
        unique_together = ['name', 'subcategory']
    
    def __str__(self):
        if self.subcategory:
            return f"{self.name} > {self.subcategory}"
        return self.name


class Part(models.Model):
    """Parça tanımı - gerçek saha kurallarına göre"""
    workshop = models.ForeignKey(
        'workshops.Workshop',
        on_delete=models.CASCADE,
        related_name='parts',
        verbose_name='Dükkân'
    )
    
    # ZORUNLU ALANLAR
    name = models.CharField(max_length=200, verbose_name='Parça Adı (Usta Dili)')
    category = models.ForeignKey(
        PartCategory,
        on_delete=models.PROTECT,
        related_name='parts',
        verbose_name='Kategori'
    )
    
    # OPSİYONEL ALANLAR
    brand = models.CharField(max_length=100, blank=True, verbose_name='Marka (OEM/Muadil/Üretici)')
    code = models.CharField(max_length=100, blank=True, verbose_name='Parça Kodu (Opsiyonel)')
    auto_code = models.CharField(max_length=100, unique=True, editable=False, verbose_name='Otomatik Kod')
    image = models.ImageField(upload_to='parts/', null=True, blank=True, verbose_name='Görsel')
    
    # STOK BİLGİLERİ
    quantity = models.IntegerField(
        default=0,
        validators=[MinValueValidator(0)],
        verbose_name='Stok Miktarı'
    )
    min_stock = models.IntegerField(
        default=1,
        validators=[MinValueValidator(0)],
        verbose_name='Minimum Stok'
    )
    
    # FİYAT BİLGİLERİ (güncel)
    current_purchase_price = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        null=True,
        blank=True,
        verbose_name='Güncel Alış Fiyatı'
    )
    current_sale_price = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        null=True,
        blank=True,
        verbose_name='Güncel Satış Fiyatı'
    )
    
    is_active = models.BooleanField(default=True, verbose_name='Aktif')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='Oluşturulma Tarihi')
    updated_at = models.DateTimeField(auto_now=True, verbose_name='Güncellenme Tarihi')
    
    class Meta:
        verbose_name = 'Parça'
        verbose_name_plural = 'Parçalar'
        ordering = ['name']
        indexes = [
            models.Index(fields=['name']),
            models.Index(fields=['code']),
            models.Index(fields=['auto_code']),
        ]
    
    def save(self, *args, **kwargs):
        if not self.auto_code:
            # Otomatik kod üret: PAR-{UUID kısa}
            self.auto_code = f"PAR-{uuid.uuid4().hex[:8].upper()}"
        super().save(*args, **kwargs)
    
    def __str__(self):
        return f"{self.name} ({self.category})"
    
    @property
    def is_low_stock(self):
        return self.quantity <= self.min_stock
    
    @property
    def average_purchase_price(self):
        """Ortalama alış maliyeti"""
        purchases = PurchasePrice.objects.filter(part=self)
        if purchases.exists():
            total = sum(p.price for p in purchases)
            return total / purchases.count()
        return self.current_purchase_price or 0
    
    @property
    def profit_percentage(self):
        """Kâr yüzdesi"""
        if self.current_purchase_price and self.current_sale_price:
            if self.current_purchase_price > 0:
                profit = self.current_sale_price - self.current_purchase_price
                return (profit / self.current_purchase_price) * 100
        return 0


class PartCompatibility(models.Model):
    """Parça-araç uyumluluğu"""
    part = models.ForeignKey(
        Part,
        on_delete=models.CASCADE,
        related_name='compatibilities',
        verbose_name='Parça'
    )
    vehicle = models.ForeignKey(
        Vehicle,
        on_delete=models.CASCADE,
        related_name='compatible_parts',
        verbose_name='Araç'
    )
    
    class Meta:
        verbose_name = 'Parça Uyumluluğu'
        verbose_name_plural = 'Parça Uyumlulukları'
        unique_together = ['part', 'vehicle']
        ordering = ['vehicle__brand', 'vehicle__model']
    
    def __str__(self):
        return f"{self.part.name} → {self.vehicle}"


class AlternativePart(models.Model):
    """Muadil/Alternatif parça ilişkisi"""
    part = models.ForeignKey(
        Part,
        on_delete=models.CASCADE,
        related_name='alternatives',
        verbose_name='Parça'
    )
    alternative = models.ForeignKey(
        Part,
        on_delete=models.CASCADE,
        related_name='alternative_for',
        verbose_name='Alternatif Parça'
    )
    note = models.TextField(blank=True, verbose_name='Not')
    
    class Meta:
        verbose_name = 'Alternatif Parça'
        verbose_name_plural = 'Alternatif Parçalar'
        unique_together = ['part', 'alternative']
    
    def __str__(self):
        return f"{self.part.name} ↔ {self.alternative.name}"


class PartNote(models.Model):
    """Parça notları - usta notları"""
    part = models.ForeignKey(
        Part,
        on_delete=models.CASCADE,
        related_name='notes',
        verbose_name='Parça'
    )
    note = models.TextField(verbose_name='Not')
    created_by = models.ForeignKey(
        'users.CustomUser',
        on_delete=models.SET_NULL,
        null=True,
        related_name='part_notes',
        verbose_name='Yazan'
    )
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='Tarih')
    
    class Meta:
        verbose_name = 'Parça Notu'
        verbose_name_plural = 'Parça Notları'
        ordering = ['-created_at']
    
    def __str__(self):
        return f"{self.part.name} - {self.created_at.strftime('%d.%m.%Y')}"


class PurchasePrice(models.Model):
    """Alış fiyat geçmişi"""
    part = models.ForeignKey(
        Part,
        on_delete=models.CASCADE,
        related_name='purchase_prices',
        verbose_name='Parça'
    )
    price = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        verbose_name='Alış Fiyatı'
    )
    quantity = models.IntegerField(
        validators=[MinValueValidator(1)],
        verbose_name='Miktar'
    )
    supplier = models.CharField(max_length=200, blank=True, verbose_name='Tedarikçi')
    note = models.TextField(blank=True, verbose_name='Not')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='Tarih')
    created_by = models.ForeignKey(
        'users.CustomUser',
        on_delete=models.SET_NULL,
        null=True,
        verbose_name='Oluşturan'
    )
    
    class Meta:
        verbose_name = 'Alış Fiyatı'
        verbose_name_plural = 'Alış Fiyatları'
        ordering = ['-created_at']
    
    def __str__(self):
        return f"{self.part.name} - {self.price} TL ({self.created_at.strftime('%d.%m.%Y')})"


class SalePrice(models.Model):
    """Satış fiyat geçmişi"""
    part = models.ForeignKey(
        Part,
        on_delete=models.CASCADE,
        related_name='sale_prices',
        verbose_name='Parça'
    )
    price = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        verbose_name='Satış Fiyatı'
    )
    quantity = models.IntegerField(
        validators=[MinValueValidator(1)],
        verbose_name='Miktar'
    )
    customer = models.CharField(max_length=200, blank=True, verbose_name='Müşteri')
    note = models.TextField(blank=True, verbose_name='Not')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='Tarih')
    created_by = models.ForeignKey(
        'users.CustomUser',
        on_delete=models.SET_NULL,
        null=True,
        verbose_name='Oluşturan'
    )
    
    class Meta:
        verbose_name = 'Satış Fiyatı'
        verbose_name_plural = 'Satış Fiyatları'
        ordering = ['-created_at']
    
    def __str__(self):
        return f"{self.part.name} - {self.price} TL ({self.created_at.strftime('%d.%m.%Y')})"


class StockMovement(models.Model):
    """Stok hareketi"""
    MOVEMENT_TYPE = [
        ('purchase', 'Alış'),
        ('sale', 'Satış'),
        ('return', 'İade'),
        ('adjustment', 'Manuel Düzeltme'),
    ]
    
    part = models.ForeignKey(
        Part,
        on_delete=models.CASCADE,
        related_name='movements',
        verbose_name='Parça'
    )
    movement_type = models.CharField(
        max_length=20,
        choices=MOVEMENT_TYPE,
        verbose_name='Hareket Türü'
    )
    quantity = models.IntegerField(
        validators=[MinValueValidator(1)],
        verbose_name='Miktar'
    )
    note = models.TextField(blank=True, verbose_name='Not')
    created_by = models.ForeignKey(
        'users.CustomUser',
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        verbose_name='Oluşturan'
    )
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='Oluşturulma Tarihi')
    
    class Meta:
        verbose_name = 'Stok Hareketi'
        verbose_name_plural = 'Stok Hareketleri'
        ordering = ['-created_at']
    
    def __str__(self):
        return f"{self.part.name} - {self.get_movement_type_display()} ({self.quantity})"
