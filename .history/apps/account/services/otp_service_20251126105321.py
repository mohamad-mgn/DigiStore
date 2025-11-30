import secrets
from django.utils import timezone
from datetime import timedelta
from apps.account.models import MobileOTP
import hashlib

class OTPService:
    """
    OTPService provides utilities to generate, send, hash, and validate
    One-Time Passwords (OTPs) for mobile authentication.
    """

    @staticmethod
    def generate_otp():
        # Generate a 6-digit numeric OTP using a cryptographically secure method
        otp = ''.join(str(secrets.randbelow(10)) for _ in range(6))
        return otp

    @staticmethod
    def hash_otp(otp: str) -> str:
        # Hash the OTP using SHA-256 for secure storage in the database
        return hashlib.sha256(otp.encode()).hexdigest()

    @staticmethod
    def send_otp(phone: str) -> str:
        # Generate and hash OTP
        code = OTPService.generate_otp()
        hashed_code = OTPService.hash_otp(code)

        # Create or update the OTP record for the given phone number
        MobileOTP.objects.update_or_create(
            phone=phone,
            defaults={
                "code": hashed_code,
                "verified": False,
                "attempts": 0,
                "created_at": timezone.now(),
            }
        )

        # Print OTP to console (for development/testing purposes)
        print("📩 OTP:", code)
        return code

    @staticmethod
    def validate_otp(phone: str, code: str) -> tuple:
        # Attempt to retrieve OTP record for the given phone
        try:
            otp = MobileOTP.objects.get(phone=phone)
        except MobileOTP.DoesNotExist:
            return False, "کد معتبر نیست."

        # Check if the OTP has expired (valid for 5 minutes)
        if timezone.now() > otp.created_at + timedelta(minutes=5):
            return False, "کد منقضی شده است."

        # Check if the maximum number of attempts has been reached
        if otp.attempts >= 5:
            return False, "تعداد تلاش بیش از حد مجاز."

        # Increment the number of attempts
        otp.increment_attempts()

        # Compare hashed OTPs
        if otp.code != OTPService.hash_otp(code):
            return False, "کد اشتباه است."

        # Mark OTP as verified
        otp.mark_verified()
        return True, "کد صحیح است."