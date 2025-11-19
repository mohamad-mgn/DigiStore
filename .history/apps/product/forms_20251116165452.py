from django import forms
from .models import Product

class ProductForm(forms.ModelForm):
    class Meta:
        model = Product
        fields = ["title", "description", "price", "stock", "image", "category"]
        labels = {
            "title": "نام محصول",
            "description": "توضیحات",
            "price": "قیمت (تومان)",
            "stock": "موجودی",
            "image": "تصویر محصول",
            "category": "دسته‌بندی",
        }
        widgets = {
            "description": forms.Textarea(attrs={"rows": 3}),
        }

    def clean_price(self):
        price = self.cleaned_data.get("price")
        if price <= 0:
            raise forms.ValidationError("قیمت باید بزرگتر از صفر باشد.")
        return price