from django import forms
from .models import Store


class StoreForm(forms.ModelForm):
    class Meta:
        model = Store
        # Fields to be included in the form
        fields = ["store_name", "description"]
        # Labels for form fields (kept in Persian)
        labels = {
            "store_name": "نام فروشگاه",
            "description": "توضیحات فروشگاه",
        }
        # Widgets for customizing form field rendering
        widgets = {
            "description": forms.Textarea(attrs={"rows": 3}),
        }