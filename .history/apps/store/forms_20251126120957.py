from django import forms
from .models import Store

# Form for creating and updating a Store
class StoreForm(forms.ModelForm):
    class Meta:
        model = Store
        fields = ["store_name", "description"]
        labels = {
            "store_name": "Store Name",
            "description": "Store Description",
        }
        widgets = {
            "description": forms.Textarea(attrs={"rows": 3}),
        }