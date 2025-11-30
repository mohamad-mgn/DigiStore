from django.db import models
from apps.user.models import SellerProfile
from django.utils.text import slugify

class Store(models.Model):
    """
    مدل فروشگاه: هر فروشنده می‌تواند چند Store داشته باشد.
    فیلد slug برای آدرس خوانا استفاده می‌شود.
    """
    seller = models.ForeignKey(SellerProfile, on_delete=models.CASCADE, related_name='stores')
    name = models.CharField('نام فروشگاه', max_length=255)
    slug = models.SlugField('نشانی', unique=True, max_length=255)
    description = models.TextField('توضیحات', blank=True)
    address = models.TextField('آدرس', blank=True)
    logo = models.ImageField('لوگو', upload_to='store_logos/', blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def save(self, *args, **kwargs):
        # اگر slug خالی است، از نام slugify بساز
        if not self.slug:
            self.slug = slugify(self.name)
        super().save(*args, **kwargs)

    def __str__(self):
        return self.name