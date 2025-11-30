from django.db import models
from django.utils import timezone
from django.conf import settings
from apps.user.models import User
from apps.product.models import Product


class Order(models.Model):
    STATUS_CHOICES = [
        ('pending', 'در انتظار پرداخت'),
        ('paid', 'پرداخت شده'),
        ('processing', 'در حال پردازش'),
        ('shipped', 'ارسال شده'),
        ('completed', 'تکمیل‌شده'),
        ('cancelled', 'لغو شده'),
    ]

    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="orders", verbose_name="خریدار")
    status = models.CharField("وضعیت", max_length=20, choices=STATUS_CHOICES, default='pending')
    total_amount = models.PositiveIntegerField("مبلغ کل (تومان)", default=0)
    created_at = models.DateTimeField("تاریخ ایجاد", default=timezone.now)
    updated_at = models.DateTimeField("آخرین تغییر", auto_now=True)

    # آدرس (در صورت نیاز می‌توان مدل Address جداگانه ساخت)
    address = models.CharField("آدرس تحویل", max_length=255, blank=True, null=True)
    postal_code = models.CharField("کد پستی", max_length=20, blank=True, null=True)

    def __str__(self):
        return f"Order #{self.id} - {self.user.phone}"

    class Meta:
        verbose_name = "سفارش"
        verbose_name_plural = "سفارش‌ها"
        ordering = ['-created_at']


class OrderItem(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE, related_name="items", verbose_name="سفارش")
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name="order_items", verbose_name="محصول")
    unit_price = models.PositiveIntegerField("قیمت واحد (تومان)")
    quantity = models.PositiveIntegerField("تعداد", default=1)

    class Meta:
        verbose_name = "آیتم سفارش"
        verbose_name_plural = "آیتم‌های سفارش"

    def __str__(self):
        return f"{self.product.title} × {self.quantity}"

    @property
    def total_price(self):
        return self.unit_price * self.quantity