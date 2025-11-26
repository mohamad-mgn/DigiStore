from django.db import models
from django.utils import timezone
from datetime import timedelta

# --------------------------------------------------------
# MobileOTP Model
# --------------------------------------------------------
class MobileOTP(models.Model):
    """
    Model to store OTP (One-Time Password) codes for mobile authentication.
    Tracks phone number, hashed OTP code, creation time, verification status, and number of attempts.
    """

    # Phone number associated with the OTP
    phone = models.CharField("شماره موبایل", max_length=15, db_index=True)

    # Hashed OTP code (stored securely)
    code = models.CharField("کد", max_length=64)

    # Timestamp when the OTP was created
    created_at = models.DateTimeField("تاریخ ایجاد", default=timezone.now)

    # Flag indicating whether the OTP has been verified
    verified = models.BooleanField("تأیید شده", default=False)

    # Counter for the number of validation attempts
    attempts = models.PositiveSmallIntegerField("تعداد تلاش‌ها", default=0)

    class Meta:
        # Human-readable singular and plural names for the admin interface
        verbose_name = "کد تأیید"
        verbose_name_plural = "کدهای تأیید"

        # Database indexes for faster lookups
        indexes = [
            models.Index(fields=["phone", "created_at"]),
        ]

    def __str__(self):
        # String representation of the OTP instance
        return f"{self.phone} - {self.code}"

    def is_expired(self):
        """
        Check whether the OTP has expired.
        OTPs are valid for 5 minutes from creation.
        """
        return timezone.now() > self.created_at + timedelta(minutes=5)

    def mark_verified(self):
        """
        Mark the OTP as verified and save the change to the database.
        """
        self.verified = True
        self.save(update_fields=["verified"])

    def increment_attempts(self):
        """
        Increment the attempts counter by 1 and save to the database.
        """
        self.attempts += 1
        self.save(update_fields=["attempts"])