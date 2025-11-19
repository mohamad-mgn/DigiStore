from django.db import models
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin
from django.utils import timezone
from .managers import UserManager

class User(AbstractBaseUser, PermissionsMixin):
    """
    مدل کاربر سفارشی: شماره موبایل (phone) به عنوان شناسه کاربری
    فیلدهای پایه: phone, full_name, email, is_active, is_staff, created_at
    """
    phone = models.CharField('شماره موبایل', max_length=15, unique=True)
    full_name = models.CharField('نام و نام خانوادگی', max_length=150, blank=True, null=True)
    email = models.EmailField('ایمیل', blank=True, null=True)
    is_active = models.BooleanField('فعال', default=True)
    is_staff = models.BooleanField('کارمند', default=False)
    created_at = models.DateTimeField('تاریخ ایجاد', default=timezone.now)

    objects = UserManager()

    USERNAME_FIELD = 'phone'
    REQUIRED_FIELDS = []

    def __str__(self):
        return self.full_name or self.phone

class CustomerProfile(models.Model):
    """
    پروفایل خریدار — اطلاعات تکمیلی که بعداً قابل گسترش است
    """
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='customer_profile')
    address = models.TextField('آدرس', blank=True, null=True)
    postal_code = models.CharField('کد پستی', max_length=20, blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"CustomerProfile: {self.user.phone}"

class SellerProfile(models.Model):
    """
    پروفایل فروشنده — اطلاعات شخصی فروشنده که قابل تکمیل است
    توجه: فروشنده ممکن است چند فروشگاه داشته باشد.
    """
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='seller_profile')
    national_id = models.CharField('کدملی / شناسه فروشنده', max_length=50, blank=True, null=True)
    bio = models.TextField('درباره فروشنده', blank=True, null=True)
    phone = models.CharField('تلفن فروشگاه', max_length=15, blank=True, null=True)
    address = models.TextField('آدرس فروشنده', blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"SellerProfile: {self.user.phone}"