from django.db import models
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin
from django.utils import timezone

from .managers import UserManager


# Custom user model using phone number as the username
class User(AbstractBaseUser, PermissionsMixin):
    phone = models.CharField(
        max_length=15,
        unique=True,
        verbose_name="شماره موبایل",
        help_text="ورود و احراز هویت با این شماره انجام می‌شود."  # Used for login and authentication
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

    is_active = models.BooleanField("فعال", default=True)  # Whether the user account is active
    is_staff = models.BooleanField("استفاده از ادمین", default=False)  # Admin access
    is_seller = models.BooleanField("فروشنده", default=False)  # Seller status

    date_joined = models.DateTimeField("تاریخ عضویت", default=timezone.now)  # Account creation time

    USERNAME_FIELD = "phone"  # Set phone as login field
    REQUIRED_FIELDS = []  # No additional required fields

    objects = UserManager()  # Custom user manager

    class Meta:
        verbose_name = "کاربر"
        verbose_name_plural = "کاربران"
        ordering = ["-date_joined"]

    def __str__(self):
        return f"{self.full_name or self.phone}"  # Show full name if available, else phone number

    @property
    def name(self):
        return self.full_name or self.phone  # Convenience property for user display name


# Profile model for customer users
class CustomerProfile(models.Model):
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
        return f"پروفایل خریدار: {self.user}"  # Display user in profile


# Profile model for seller users
class SellerProfile(models.Model):
    user = models.OneToOneField(
        User,
        on_delete=models.CASCADE,
        related_name="seller_profile",
        verbose_name="کاربر"
    )

    store_name = models.CharField("نام فروشگاه", max_length=200, blank=True, null=True)
    national_id = models.CharField("کدملی", max_length=50, blank=True, null=True)
    phone_secondary = models.CharField("شماره تماس دیگر", max_length=15, blank=True, null=True)
    description = models.TextField("توضیحات فروشنده", blank=True, null=True)

    class Meta:
        verbose_name = "پروفایل فروشنده"
        verbose_name_plural = "پروفایل‌های فروشنده"

    def __str__(self):
        return f"پروفایل فروشنده: {self.user}"  # Display user in profile