from django.db import models
from apps.user.models import User


class Store(models.Model):
    # One-to-one relation to the user who is the seller
    seller = models.OneToOneField(
        User,
        on_delete=models.CASCADE,
        related_name="store",
        verbose_name="فروشنده"
    )

    # Name of the store
    store_name = models.CharField("نام فروشگاه", max_length=200)
    # Description of the store (optional)
    description = models.TextField("توضیحات فروشگاه", blank=True, null=True)

    # Timestamps
    created_at = models.DateTimeField("تاریخ ایجاد", auto_now_add=True)
    updated_at = models.DateTimeField("آخرین بروزرسانی", auto_now=True)

    class Meta:
        verbose_name = "فروشگاه"
        verbose_name_plural = "فروشگاه‌ها"
        # Default ordering: newest first
        ordering = ['-created_at']

    def __str__(self):
        # String representation of the store
        return self.store_name