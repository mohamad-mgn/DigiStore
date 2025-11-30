import random
from django.utils import timezone
from datetime import timedelta
from apps.account.models import MobileOTP


class OTPService:

    @staticmethod
    def generate_otp():
        """ساخت کد ۶ رقمی"""
        return random.randint(100000, 999999)

    @staticmethod
    def send_otp(phone: str) -> int:
        """
        ساخت و ذخیره کد OTP برای شماره موبایل
        """
        code = OTPService.generate_otp()

        MobileOTP.objects.update_or_create(
            phone=phone,
            defaults={
                "code": code,
                "verified": False,
                "attempts": 0,
                "created_at": timezone.now(),
            }
        )

        print("📩 OTP:", code)  # فعلاً بجای SMS چاپ می‌کنیم

        return code

    @staticmethod
    def validate_otp(phone: str, code: str) -> tuple[bool, str]:
        """
        بررسی صحت کد:
        - منقضی بودن
        - تعداد تلاش‌ها
        - برابر بودن
        """

        try:
            otp = MobileOTP.objects.get(phone=phone)
        except MobileOTP.DoesNotExist:
            return False, "کد معتبر نیست."

        # انقضا
        if timezone.now() > otp.created_at + timedelta(minutes=5):
            return False, "کد منقضی شده است."

        # تعداد تلاش‌ها
        if otp.attempts >= 5:
            return False, "تعداد تلاش بیش از حد مجاز."

        otp.increment_attempts()

        if str(otp.code) != str(code):
            return False, "کد اشتباه است."

        otp.mark_verified()
        return True, "کد صحیح است."