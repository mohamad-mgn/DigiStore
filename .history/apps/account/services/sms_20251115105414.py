"""
سرویس ارسال SMS — این ماژول abstraction است.
فعلاً یک implementation ساده (mock) دارد که کد را در لاگ چاپ می‌کند.
در آینده می‌توانی adapter برای Twilio/NextSMS/کافه‌بوت/ملی پیامک/هر سرویس دیگر اضافه کنی.
"""
import logging

logger = logging.getLogger(__name__)

class BaseSMSService:
    def send_code(self, phone: str, code: str) -> bool:
        """
        ارسال کد به شماره‌ی phone
        باید توسط adapter واقعی override شود.
        برگرداندن True یعنی ارسال موفق (یا قبول سرویس).
        """
        raise NotImplementedError

class MockSMSService(BaseSMSService):
    def send_code(self, phone: str, code: str) -> bool:
        # Mock behavior: فقط لاگ می‌کنیم
        logger.info(f"[MOCK SMS] send to {phone}: {code}")
        # همچنین چاپ در stdout برای توسعه محلی
        print(f"[MOCK SMS] OTP for {phone}: {code}")
        return True

# برای استفاده، import و instance بگیر:
sms_service = MockSMSService()