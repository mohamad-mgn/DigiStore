from django import forms
from .models import Store


class StoreForm(forms.ModelForm):
    class Meta:
        model = Store
        fields = ["store_name", "description"]
        labels = {
            "store_name": "نام فروشگاه",
            "description": "توضیحات فروشگاه",
        }
        widgets = {
            "description": forms.Textarea(attrs={"rows": 3}),
        }