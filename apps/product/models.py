from django.db import models
from django.utils.text import slugify
from django.urls import reverse
from apps.store.models import Store

# =========================
#   Category Model
# =========================
class Category(models.Model):
    name = models.CharField("نام دسته", max_length=120)
    slug = models.SlugField("شناسه", unique=True, blank=True)  # auto-generated if blank

    class Meta:
        verbose_name = "دسته‌بندی"
        verbose_name_plural = "دسته‌بندی‌ها"

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        super().save(*args, **kwargs)


# =========================
#   Product Model
# =========================
class Product(models.Model):
    store = models.ForeignKey(
        Store,
        on_delete=models.CASCADE,
        related_name="products",
        verbose_name="فروشگاه"
    )
    title = models.CharField("نام محصول", max_length=255)
    description = models.TextField("توضیحات", blank=True)
    price = models.PositiveIntegerField("قیمت (تومان)")
    stock = models.PositiveIntegerField("موجودی", default=0)
    image = models.ImageField(
        "تصویر محصول",
        upload_to="products/",
        blank=True,
        null=True,
        default="products/placeholder.png"
    )
    category = models.ForeignKey(
        Category,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="products",
        verbose_name="دسته‌بندی"
    )
    created_at = models.DateTimeField("تاریخ ایجاد", auto_now_add=True)
    updated_at = models.DateTimeField("آخرین تغییر", auto_now=True)

    class Meta:
        verbose_name = "محصول"
        verbose_name_plural = "محصولات"
        ordering = ["-created_at"]

    def __str__(self):
        return self.title

    # URL for the product detail page
    def get_absolute_url(self):
        return reverse("product:detail", args=[str(self.id)])