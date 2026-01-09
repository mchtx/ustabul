from django.db import models


class Conversation(models.Model):
    """Sohbet odası"""
    customer = models.ForeignKey(
        'users.CustomUser',
        on_delete=models.CASCADE,
        related_name='customer_conversations',
        verbose_name='Müşteri'
    )
    workshop = models.ForeignKey(
        'workshops.Workshop',
        on_delete=models.CASCADE,
        related_name='conversations',
        verbose_name='Dükkân'
    )
    is_active = models.BooleanField(
        default=True,
        verbose_name='Aktif'
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
        unique_together = ('customer', 'workshop')
        verbose_name = 'Sohbet'
        verbose_name_plural = 'Sohbetler'
        ordering = ['-updated_at']
    
    def __str__(self):
        return f"{self.customer.username} - {self.workshop.name}"


class Message(models.Model):
    """Mesaj"""
    conversation = models.ForeignKey(
        Conversation,
        on_delete=models.CASCADE,
        related_name='messages',
        verbose_name='Sohbet'
    )
    sender = models.ForeignKey(
        'users.CustomUser',
        on_delete=models.CASCADE,
        related_name='sent_messages',
        verbose_name='Gönderici'
    )
    content = models.TextField(
        verbose_name='İçerik'
    )
    is_read = models.BooleanField(
        default=False,
        verbose_name='Okundu'
    )
    created_at = models.DateTimeField(
        auto_now_add=True,
        verbose_name='Oluşturulma Tarihi'
    )
    
    class Meta:
        verbose_name = 'Mesaj'
        verbose_name_plural = 'Mesajlar'
        ordering = ['created_at']
    
    def __str__(self):
        return f"{self.sender.username}: {self.content[:50]}"
