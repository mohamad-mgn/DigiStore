from django import forms
import re

from apps.user.models import User, CustomerProfile, SellerProfile

# --------------------------------------------------------
# Regular expression to validate Iranian phone numbers
# Matches: 09xxxxxxxxx, +989xxxxxxxxx, 989xxxxxxxxx
# --------------------------------------------------------
PHONE_RE = re.compile(r'^(?:\+?98|0)?9\d{9}$')

# -----------------------------
#   Send OTP Form
# -----------------------------
class SendOTPForm(forms.Form):
    phone = forms.CharField(label='شماره موبایل', max_length=15)

    def clean_phone(self):
        """
        Normalize and validate the phone number.
        - Remove spaces and dashes
        - Convert +98 or 98 prefix to 0
        - Ensure the number matches Iranian mobile format
        """
        phone = self.cleaned_data['phone'].strip()
        phone = phone.replace(" ", "").replace("-", "")

        if not PHONE_RE.match(phone):
            raise forms.ValidationError("شماره موبایل معتبر نیست. مثل: 09123456789")

        if phone.startswith("+98"):
            phone = "0" + phone[3:]
        elif phone.startswith("98") and len(phone) == 12:
            phone = "0" + phone[2:]

        return phone


# -----------------------------
#   Verify OTP Form
# -----------------------------
class VerifyOTPForm(forms.Form):
    phone = forms.CharField(widget=forms.HiddenInput())
    code = forms.CharField(label="کد تایید", max_length=6)

    def clean_code(self):
        """
        Ensure the OTP code is exactly 6 digits.
        """
        code = self.cleaned_data["code"].strip()
        if not code.isdigit() or len(code) != 6:
            raise forms.ValidationError("کد باید ۶ رقمی باشد.")
        return code


# -----------------------------
#   Signup Form
# -----------------------------
class SignupForm(forms.Form):
    phone = forms.CharField(widget=forms.HiddenInput())
    full_name = forms.CharField(label='نام و نام خانوادگی', required=False)

    role = forms.ChoiceField(
        label='نقش کاربر',
        choices=(
            ('customer', 'خریدار'),
            ('seller', 'فروشنده'),
        )
    )


# -----------------------------
#   Signin Form
# -----------------------------
class SigninForm(forms.Form):
    phone = forms.CharField(label='شماره موبایل', max_length=15)


# -----------------------------
#   Edit Customer Profile Form
# -----------------------------
class EditCustomerProfileForm(forms.ModelForm):
    full_name = forms.CharField(label="نام و نام خانوادگی", required=False)

    class Meta:
        model = CustomerProfile
        fields = ["address", "postal_code"]
        labels = {
            "address": "آدرس",
            "postal_code": "کد پستی",
        }

    def save(self, user, commit=True):
        """
        Save both the user full name and customer profile.
        """
        user.full_name = self.cleaned_data.get("full_name")
        if commit:
            user.save()

        profile = super().save(commit=False)
        profile.user = user

        if commit:
            profile.save()

        return profile


# -----------------------------
#   Edit Seller Profile Form
# -----------------------------
class EditSellerProfileForm(forms.ModelForm):
    full_name = forms.CharField(label="نام و نام خانوادگی", required=False)

    class Meta:
        model = SellerProfile
        fields = ["store_name", "national_id"]
        labels = {
            "store_name": "نام فروشگاه",
            "national_id": "کد ملی",
        }

    def save(self, user, commit=True):
        """
        Save both the user full name and seller profile.
        """
        user.full_name = self.cleaned_data.get("full_name")
        if commit:
            user.save()

        profile = super().save(commit=False)
        profile.user = user
        if commit:
            profile.save()

        return profile