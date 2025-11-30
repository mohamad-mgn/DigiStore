# services/otp_service.py
import secrets
from django.utils import timezone
from datetime import timedelta
from apps.account.models import MobileOTP
import hashlib

class OTPService:

    @staticmethod
    def generate_otp():
        otp = ''.join(str(secrets.randbelow(10)) for _ in range(6))
        return otp

    @staticmethod
    def hash_otp(otp: str) -> str:
        return hashlib.sha256(otp.encode()).hexdigest()

    @staticmethod
    def send_otp(phone: str) -> str:
        code = OTPService.generate_otp()
        hashed_code = OTPService.hash_otp(code)

        MobileOTP.objects.update_or_create(
            phone=phone,
            defaults={
                "code": hashed_code,
                "verified": False,
                "attempts": 0,
                "created_at": timezone.now(),
            }
        )

        print("📩 OTP:", code)
        return code

    @staticmethod
    def validate_otp(phone: str, code: str) -> tuple:
        try:
            otp = MobileOTP.objects.get(phone=phone)
        except MobileOTP.DoesNotExist:
            return False, "کد معتبر نیست."

        if timezone.now() > otp.created_at + timedelta(minutes=5):
            return False, "کد منقضی شده است."

        if otp.attempts >= 5:
            return False, "تعداد تلاش بیش از حد مجاز."

        otp.increment_attempts()

        if otp.code != OTPService.hash_otp(code):
            return False, "کد اشتباه است."

        otp.mark_verified()
        return True, "کد صحیح است."