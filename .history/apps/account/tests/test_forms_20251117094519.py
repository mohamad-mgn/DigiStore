from django.test import TestCase
from apps.account.forms import SendOTPForm


class SendOTPFormTest(TestCase):

    def test_valid_phone(self):
        form = SendOTPForm(data={"phone": "09123456789"})
        self.assertTrue(form.is_valid())

    def test_invalid_phone(self):
        form = SendOTPForm(data={"phone": "123"})
        self.assertFalse(form.is_valid())