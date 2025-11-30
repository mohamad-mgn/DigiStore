from django.db import models
from apps.store.models import Store


class Product(models.Model):
    store = models.ForeignKey(
        Store,
        on_delete=models.CASCADE,
        related_name="products",
        verbose_name="فروشگاه"
    )
    title = models.CharField("نام محصول", max_length=200)
    description = models.TextField("توضیحات", blank=True, null=True)
    price = models.PositiveIntegerField("قیمت (تومان)")
    stock = models.PositiveIntegerField("موجودی", default=0)
    image = models.ImageField("تصویر", upload_to="products/", blank=True, null=True)
    created_at = models.DateTimeField("تاریخ ثبت", auto_now_add=True)

    class Meta:
        verbose_name = "محصول"
        verbose_name_plural = "محصولات"
        ordering = ["-created_at"]

    def __str__(self):
        return self.title