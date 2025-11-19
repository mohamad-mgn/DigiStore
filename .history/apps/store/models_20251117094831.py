# apps/store/models.py

from django.db import models
from apps.user.models import User


class Store(models.Model):
    seller = models.OneToOneField(
        User,
        on_delete=models.CASCADE,
        related_name="store",
        verbose_name="فروشنده"
    )

    store_name = models.CharField("نام فروشگاه", max_length=200)
    description = models.TextField("توضیحات فروشگاه", blank=True, null=True)

    created_at = models.DateTimeField("تاریخ ایجاد", auto_now_add=True)
    updated_at = models.DateTimeField("آخرین بروزرسانی", auto_now=True)

    class Meta:
        verbose_name = "فروشگاه"
        verbose_name_plural = "فروشگاه‌ها"
        ordering = ['-created_at']

    def __str__(self):
        return self.store_name