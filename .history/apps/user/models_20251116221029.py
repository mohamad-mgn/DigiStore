from django.db import models
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin
from django.utils import timezone

from .managers import UserManager


class User(AbstractBaseUser, PermissionsMixin):
    """
    مدل کاربر سفارشی: شناسه‌ی ورود = شماره موبایل
    فیلدهایی که نیاز داریم:
      - phone (شناسه)
      - full_name
      - email (اختیاری)
      - is_active / is_staff / is_superuser / is_seller
      - date_joined
    """

    phone = models.CharField(
        max_length=15,
        unique=True,
        verbose_name="شماره موبایل",
        help_text="ورود و احراز هویت با این شماره انجام می‌شود."
    )

    full_name = models.CharField(
        max_length=120,
        blank=True,
        null=True,
        verbose_name="نام و نام خانوادگی"
    )

    email = models.EmailField(
        verbose_name="ایمیل",
        blank=True,
        null=True
    )

    is_active = models.BooleanField("فعال", default=True)
    is_staff = models.BooleanField("استفاده از ادمین", default=False)
    is_seller = models.BooleanField("فروشنده", default=False)

    date_joined = models.DateTimeField("تاریخ عضویت", default=timezone.now)

    USERNAME_FIELD = "phone"
    REQUIRED_FIELDS = []  # فقط phone لازم است

    objects = UserManager()

    class Meta:
        verbose_name = "کاربر"
        verbose_name_plural = "کاربران"
        ordering = ["-date_joined"]

    def __str__(self):
        # نمایش کاربر در پنل ادمین و لاگ‌ها
        return f"{self.full_name or self.phone}"

    @property
    def name(self):
        """نام نمایشی"""
        return self.full_name or self.phone


class CustomerProfile(models.Model):
    """
    پروفایل خریدار — اطلاعاتی که صرفاً برای خریدار نیاز است.
    مدل جدا به خاطر توسعه‌پذیری و امکان داشتن فیلدهای مختلف در آینده.
    """
    user = models.OneToOneField(
        User,
        on_delete=models.CASCADE,
        related_name="customer_profile",
        verbose_name="کاربر"
    )
    address = models.CharField("آدرس", max_length=255, blank=True, null=True)
    postal_code = models.CharField("کد پستی", max_length=20, blank=True, null=True)

    class Meta:
        verbose_name = "پروفایل خریدار"
        verbose_name_plural = "پروفایل‌های خریدار"

    def __str__(self):
        return f"پروفایل خریدار: {self.user}"


class SellerProfile(models.Model):
    """
    پروفایل فروشنده — اطلاعاتی که فروشنده نیاز دارد.
    توجه: فروشنده هم می‌تواند نقش خریدار را داشته باشد (is_seller=True) ولی پروفایل‌ها جدا هستند.
    """
    user = models.OneToOneField(
        User,
        on_delete=models.CASCADE,
        related_name="seller_profile",
        verbose_name="کاربر"
    )

    store_name = models.CharField("نام فروشگاه", max_length=200, blank=True, null=True)
    national_id = models.CharField("شناسه/کدملی", max_length=50, blank=True, null=True)
    phone_secondary = models.CharField("شماره تماس دیگر", max_length=15, blank=True, null=True)
    description = models.TextField("توضیحات فروشنده", blank=True, null=True)

    class Meta:
        verbose_name = "پروفایل فروشنده"
        verbose_name_plural = "پروفایل‌های فروشنده"

    def __str__(self):
        return f"پروفایل فروشنده: {self.user}"