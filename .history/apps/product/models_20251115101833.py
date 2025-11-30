from django.db import models
from apps.store.models import Store

class Category(models.TextChoices):
    LAPTOP = 'laptop', 'لپ‌تاپ'
    MOBILE = 'mobile', 'موبایل'
    TABLET = 'tablet', 'تبلت'

class Product(models.Model):
    store = models.ForeignKey(Store, on_delete=models.CASCADE, related_name='products')
    title = models.CharField('عنوان', max_length=255)
    description = models.TextField('توضیحات', blank=True)
    price = models.DecimalField('قیمت', max_digits=12, decimal_places=2)
    category = models.CharField('دسته‌بندی', max_length=20, choices=Category.choices)
    stock = models.PositiveIntegerField('موجودی', default=0)
    image = models.ImageField('عکس', upload_to='products/', blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title