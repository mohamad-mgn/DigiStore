from django.db import models
from django.utils.text import slugify
from apps.user.models import User


class Store(models.Model):
    seller = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name="stores",
        verbose_name="فروشنده"
    )

    store_name = models.CharField("نام فروشگاه", max_length=200)
    slug = models.SlugField("شناسه فروشگاه", unique=True, blank=True)
    description = models.TextField("توضیحات", blank=True, null=True)

    created_at = models.DateTimeField("تاریخ ایجاد", auto_now_add=True)
    updated_at = models.DateTimeField("آخرین تغییر", auto_now=True)

    class Meta:
        verbose_name = "فروشگاه"
        verbose_name_plural = "فروشگاه‌ها"
        ordering = ['-created_at']

    def __str__(self):
        return self.store_name

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.store_name)
        super().save(*args, **kwargs)