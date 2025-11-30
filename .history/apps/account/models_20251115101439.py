from django.db import models
from django.utils import timezone

class MobileOTP(models.Model):
    """
    ذخیرهٔ کد OTP برای شماره‌ها (mock)
    """
    phone = models.CharField(max_length=15)
    code = models.CharField(max_length=6)
    created_at = models.DateTimeField(default=timezone.now)
    verified = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.phone} - {self.code}"