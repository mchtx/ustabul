from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator


class Review(models.Model):
    """Yorum ve puanlama"""
    user = models.ForeignKey(
        'users.CustomUser',
        on_delete=models.CASCADE,
        related_name='reviews',
        verbose_name='Kullanıcı'
    )
    workshop = models.ForeignKey(
        'workshops.Workshop',
        on_delete=models.CASCADE,
        related_name='reviews',
        verbose_name='Dükkân'
    )
    rating = models.IntegerField(
        validators=[MinValueValidator(1), MaxValueValidator(5)],
        verbose_name='Puan'
    )
    comment = models.TextField(
        blank=True,
        verbose_name='Yorum'
    )
    is_verified = models.BooleanField(
        default=False,
        verbose_name='Doğrulanmış'
    )
    is_approved = models.BooleanField(
        default=True,
        verbose_name='Onaylı'
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
        verbose_name = 'Yorum'
        verbose_name_plural = 'Yorumlar'
        ordering = ['-created_at']
    
    def __str__(self):
        return f"{self.user.username} - {self.workshop.name} ({self.rating}★)"


class ReviewReply(models.Model):
    """İşletme yanıtı"""
    review = models.ForeignKey(
        Review,
        on_delete=models.CASCADE,
        related_name='reply',
        verbose_name='Yorum'
    )
    workshop_owner = models.ForeignKey(
        'users.CustomUser',
        on_delete=models.CASCADE,
        related_name='review_replies',
        verbose_name='İşletme Sahibi'
    )
    comment = models.TextField(
        verbose_name='Yanıt'
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
        verbose_name = 'Yorum Yanıtı'
        verbose_name_plural = 'Yorum Yanıtları'
    
    def __str__(self):
        return f"Yanıt - {self.review.workshop.name}"
