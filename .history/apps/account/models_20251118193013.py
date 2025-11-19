from django.db import models
from django.utils import timezone
from datetime import timedelta


class MobileOTP(models.Model):
    phone = models.CharField("شماره موبایل", max_length=15, db_index=True)
    code = models.CharField("کد", max_length=64)
    created_at = models.DateTimeField("تاریخ ایجاد", default=timezone.now)
    verified = models.BooleanField("تأیید شده", default=False)
    attempts = models.PositiveSmallIntegerField("تعداد تلاش‌ها", default=0)

    class Meta:
        verbose_name = "کد تأیید"
        verbose_name_plural = "کدهای تأیید"
        indexes = [
            models.Index(fields=["phone", "created_at"]),
        ]

    def __str__(self):
        return f"{self.phone} - {self.code}"

    def is_expired(self):
        return timezone.now() > self.created_at + timedelta(minutes=5)

    def mark_verified(self):
        self.verified = True
        self.save(update_fields=["verified"])

    def increment_attempts(self):
        self.attempts += 1
        self.save(update_fields=["attempts"])