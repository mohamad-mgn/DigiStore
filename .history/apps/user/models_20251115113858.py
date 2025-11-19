from django.db import models
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin
from django.utils import timezone
from .managers import UserManager


class User(AbstractBaseUser, PermissionsMixin):
    """
    مدل کاربر سفارشی سایت — ورود با شماره موبایل.
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

    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)  # برای دسترسی به داشبورد ادمین
    is_seller = models.BooleanField(default=False)  # نقش فروشنده

    date_joined = models.DateTimeField(default=timezone.now)

    USERNAME_FIELD = "phone"
    REQUIRED_FIELDS = []  # چون فقط phone مهم است

    objects = UserManager()

    class Meta:
        verbose_name = "کاربر"
        verbose_name_plural = "کاربران"

    def __str__(self):
        return self.phone

    @property
    def name(self):
        """نمایش اسم — اگر خالی بود، شماره موبایل برگردان"""
        return self.full_name or self.phone

    def promote_to_seller(self):
        """تبدیل کاربر به فروشنده (برای پنل مدیریت فروشندگان)"""
        self.is_seller = True
        self.save(update_fields=['is_seller'])