from django.test import TestCase
from django.urls import reverse


class OTPViewTest(TestCase):

    def test_send_otp_page_loads(self):
        response = self.client.get(reverse("account:send_otp"))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "شماره موبایل")