from django.contrib import admin
from .models import Product, Category


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ("name", "slug")
    prepopulated_fields = {"slug": ("name",)}
    search_fields = ("name",)
    empty_value_display = "-خالی-"


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

    list_filter = ('store', 'category', 'created_at')
    search_fields = ('title', 'description')
    ordering = ('-created_at',)
    list_editable = ("price", "stock")
    empty_value_display = "-خالی-"