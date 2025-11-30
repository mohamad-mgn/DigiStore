from django import forms
from .models import CustomerProfile, SellerProfile, User

# Form to update the main user fields
class UserUpdateForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ["full_name", "email"]  # Fields that can be updated
        labels = {
            "full_name": "نام و نام خانوادگی",  # Full name label
            "email": "ایمیل",  # Email label
        }

# Form to update customer-specific profile information
class CustomerProfileForm(forms.ModelForm):
    class Meta:
        model = CustomerProfile
        fields = ["address", "postal_code"]  # Fields for customer profile
        labels = {
            "address": "آدرس",  # Address label
            "postal_code": "کد پستی",  # Postal code label
        }

# Form to update seller-specific profile information
class SellerProfileForm(forms.ModelForm):
    class Meta:
        model = SellerProfile
        fields = ["store_name", "national_id", "phone_secondary", "description"]  # Seller profile fields
        labels = {
            "store_name": "نام فروشگاه",  # Store name label
            "national_id": "کدملی",  # National ID label
            "phone_secondary": "شماره تماس دیگر",  # Secondary phone number label
            "description": "توضیحات",  # Description label
        }
        widgets = {
            "description": forms.Textarea(attrs={"rows": 4}),  # Use a textarea with 4 rows for description
        }