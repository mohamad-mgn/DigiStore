from django.db import models
from django.utils import timezone
from datetime import timedelta

class MobileOTP(models.Model):
    """
    Mobile OTP model:
    - phone: شماره موبایل مقصد
    - code: کد 6 رقمی
    - created_at: زمان ایجاد
    - verified: آیا کد تایید شده؟
    - attempts: تعداد تلاش‌های چک کردن کد (برای جلوگیری از brute force)
    """
    phone = models.CharField(max_length=15, db_index=True)
    code = models.CharField(max_length=6)
    created_at = models.DateTimeField(default=timezone.now)
    verified = models.BooleanField(default=False)
    attempts = models.PositiveSmallIntegerField(default=0)

    class Meta:
        indexes = [
            models.Index(fields=['phone', 'created_at']),
        ]

    def is_expired(self) -> bool:
        # مدت اعتبار کد: 5 دقیقه
        return timezone.now() > self.created_at + timedelta(minutes=5)

    def mark_verified(self):
        self.verified = True
        self.save(update_fields=['verified'])

    def increment_attempts(self):
        self.attempts += 1
        self.save(update_fields=['attempts'])