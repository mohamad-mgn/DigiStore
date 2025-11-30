from django.contrib import admin
from .models import Product


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ('title', 'price', 'stock', 'store', 'created_at', 'updated_at')
    list_filter = ('store',)
    search_fields = ('title', 'description')
    ordering = ('-created_at',)