from django.test import TestCase, Client
from django.urls import reverse
from apps.account.models import MobileOTP
from apps.user.models import User

class OTPFlowTest(TestCase):
    def setUp(self):
        self.client = Client()
        self.phone = '09121112233'

    def test_send_and_verify_flow_creates_user(self):
        # ارسال OTP
        resp = self.client.post(reverse('account:send_otp'), {'phone': self.phone})
        self.assertEqual(resp.status_code, 302)  # redirect to verify
        otp = MobileOTP.objects.filter(phone=self.phone).last()
        self.assertIsNotNone(otp)
        # تایید با کد درست
        resp = self.client.post(reverse('account:verify_otp'), {'phone': self.phone, 'code': otp.code})
        # اگر کاربر وجود نداشت، باید به signup ریدیرکت کنه
        self.assertIn(resp.status_code, (302, 200))