from django import forms
from .models import Product, Category

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
        
    VALID_CATEGORIES = ["laptop", "mobile", "tablet"]

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields["category"].queryset = Category.objects.filter(slug__in=self.VALID_CATEGORIES)
        
    def clean_price(self):
        price = self.cleaned_data.get("price")
        if not isinstance(price, int) or price <= 0:
            raise forms.ValidationError("قیمت باید عدد صحیح مثبت و بزرگتر از صفر باشد.")
        return price

    def clean_stock(self):
        stock = self.cleaned_data.get("stock")
        if stock < 0:
            raise forms.ValidationError("موجودی نمی‌تواند منفی باشد.")
        return stock
