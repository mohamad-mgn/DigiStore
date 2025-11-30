from django.test import TestCase
from apps.account.services.otp_service import OTPService
from apps.account.models import MobileOTP


class OTPServiceTest(TestCase):

    def test_send_otp(self):
        phone = "09123456789"
        code = OTPService.send_otp(phone)

        otp = MobileOTP.objects.get(phone=phone)
        self.assertEqual(int(otp.code), code)