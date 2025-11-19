from django import forms
from .models import CustomerProfile, SellerProfile, User

class UserUpdateForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ["full_name", "email"]
        labels = {
            "full_name": "نام و نام خانوادگی",
            "email": "ایمیل",
        }

class CustomerProfileForm(forms.ModelForm):
    class Meta:
        model = CustomerProfile
        fields = ["address", "postal_code"]
        labels = {
            "address": "آدرس",
            "postal_code": "کد پستی",
        }

class SellerProfileForm(forms.ModelForm):
    class Meta:
        model = SellerProfile
        fields = ["store_name", "national_id", "phone_secondary", "description"]
        labels = {
            "store_name": "نام فروشگاه",
            "national_id": "کدملی / شناسه",
            "phone_secondary": "شماره تماس دیگر",
            "description": "توضیحات",
        }
        widgets = {
            "description": forms.Textarea(attrs={"rows": 4}),
        }