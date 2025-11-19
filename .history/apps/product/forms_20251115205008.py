from django import forms
from .models import Product

class ProductForm(forms.ModelForm):

    class Meta:
        model = Product
        fields = ["title", "description", "price", "stock", "image"]
        labels = {
            "title": "نام محصول",
            "description": "توضیحات",
            "price": "قیمت",
            "stock": "موجودی",
            "image": "تصویر محصول",
        }