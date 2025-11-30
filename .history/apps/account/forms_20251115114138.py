from django import forms
import re

PHONE_RE = re.compile(r'^(?:\+?98|0)?9\d{9}$')  # الگوی اولیه برای شماره موبایل ایران؛ در صورت نیاز تغییر بده

class SendOTPForm(forms.Form):
    phone = forms.CharField(label='شماره موبایل', max_length=15)

    def clean_phone(self):
        phone = self.cleaned_data['phone'].strip()
        # نرمالایز: اگر با 0 شروع شده، آن را به فرمت 09... نگه دار
        # می‌توانی normalization پیچیده‌تر اضافه کنی
        phone = phone.replace(' ', '').replace('-', '')
        if not PHONE_RE.match(phone):
            raise forms.ValidationError('شماره موبایل نامعتبر است. مثال: 09121234567')
        # تبدیل +989121234567 -> 09121234567
        if phone.startswith('+98'):
            phone = '0' + phone[3:]
        if phone.startswith('98') and len(phone) == 12:
            phone = '0' + phone[2:]
        return phone

class VerifyOTPForm(forms.Form):
    phone = forms.CharField(widget=forms.HiddenInput())
    code = forms.CharField(label='کد تایید', max_length=6)

    def clean_code(self):
        code = self.cleaned_data['code'].strip()
        if not code.isdigit() or len(code) != 6:
            raise forms.ValidationError('کد باید ۶ رقمی باشد.')
        return code

class SignupForm(forms.Form):
    phone = forms.CharField(widget=forms.HiddenInput())
    full_name = forms.CharField(label='نام و نام خانوادگی', required=False)
    role = forms.ChoiceField(label='نقش', choices=(('customer', 'خریدار'), ('seller', 'فروشنده')))

class SigninForm(forms.Form):
    phone = forms.CharField(label='شماره موبایل', max_length=15)

class EditProfileForm(forms.Form):
    full_name = forms.CharField(label="نام", required=False)
    address = forms.CharField(label="آدرس", required=False)
    postal_code = forms.CharField(label="کد پستی", required=False)

    def save(self, user):
        user.full_name = self.cleaned_data['full_name']
        user.save()

        # بروزرسانی پروفایل خریدار
        cp = user.customer_profile
        cp.address = self.cleaned_data['address']
        cp.postal_code = self.cleaned_data['postal_code']
        cp.save()