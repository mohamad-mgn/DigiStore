from django.db import models
from django.utils import timezone
from apps.orders.models import Order


class Payment(models.Model):
    STATUS_CHOICES = [
        ('initiated', 'شروع‌شده'),
        ('success', 'موفق'),
        ('failed', 'ناموفق'),
    ]

    order = models.OneToOneField(Order, on_delete=models.CASCADE, related_name="payment", verbose_name="سفارش")
    amount = models.PositiveIntegerField("مبلغ (تومان)")
    status = models.CharField("وضعیت", max_length=20, choices=STATUS_CHOICES, default='initiated')
    transaction_id = models.CharField("شناسه تراکنش", max_length=255, blank=True, null=True)
    gateway = models.CharField("درگاه", max_length=50, default="mock")
    created_at = models.DateTimeField("تاریخ ایجاد", default=timezone.now)
    updated_at = models.DateTimeField("آخرین تغییر", auto_now=True)

    class Meta:
        verbose_name = "پرداخت"
        verbose_name_plural = "پرداخت‌ها"

    def __str__(self):
        return f"Payment #{self.id} - Order #{self.order.id} - {self.status}"