from django.db import models
from django.conf import settings

class Store(models.Model):
    seller = models.OneToOneField(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        verbose_name="صاحب فروشگاه"
    )
    store_name = models.CharField("نام فروشگاه", max_length=150)
    description = models.TextField("توضیحات", blank=True, null=True)
    created_at = models.DateTimeField("تاریخ ایجاد", auto_now_add=True)

    class Meta:
        verbose_name = "فروشگاه"
        verbose_name_plural = "فروشگاه‌ها"

    def __str__(self):
        return self.store_name