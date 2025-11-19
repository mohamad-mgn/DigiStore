from django.contrib import admin
from .models import Product, Category


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ("title", "slug")
    prepopulated_fields = {"slug": ("title",)}


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = (
        'title',
        'price',
        'stock',
        'store',
        'category',
        'created_at',
        'updated_at',
    )

    list_filter = ('store', 'category')
    search_fields = ('title', 'description')
    ordering = ('-created_at',)