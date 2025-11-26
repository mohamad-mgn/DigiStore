from django.db import models
from django.utils import timezone
from apps.orders.models import Order

# ========================================================
# Payment model to track order payments
# ========================================================
class Payment(models.Model):
    # Possible statuses for a payment
    STATUS_CHOICES = [
        ('initiated', 'شروع‌شده'),
        ('success', 'موفق'),
        ('failed', 'ناموفق'),
    ]

    # Link to the corresponding order (one-to-one)
    order = models.OneToOneField(
        Order, 
        on_delete=models.CASCADE, 
        related_name="payment", 
        verbose_name="سفارش"
    )

    # Payment amount in Toman
    amount = models.PositiveIntegerField("مبلغ (تومان)")

    # Current status of the payment
    status = models.CharField(
        "وضعیت", 
        max_length=20, 
        choices=STATUS_CHOICES, 
        default='initiated'
    )

    # Unique transaction ID from the payment gateway
    transaction_id = models.CharField(
        "شناسه تراکنش", 
        max_length=255, 
        blank=True, 
        null=True
    )

    # Payment gateway name (mock or real)
    gateway = models.CharField("درگاه", max_length=50, default="mock")

    # Timestamps
    created_at = models.DateTimeField("تاریخ ایجاد", default=timezone.now)
    updated_at = models.DateTimeField("آخرین تغییر", auto_now=True)

    class Meta:
        verbose_name = "پرداخت"
        verbose_name_plural = "پرداخت‌ها"

    def __str__(self):
        return f"Payment #{self.id} - Order #{self.order.id} - {self.status}"