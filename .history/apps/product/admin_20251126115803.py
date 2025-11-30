from django.contrib import admin
from .models import Product, Category


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    """Admin settings for product categories."""
    
    list_display = ("name", "slug")  # Columns to display in the list
    prepopulated_fields = {"slug": ("name",)}  # Auto-fill slug from name
    search_fields = ("name",)  # Enable search by category name
    empty_value_display = "-خالی-"  # Display for empty fields


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    """Admin settings for products."""
    
    list_display = (
        'title',
        'price',
        'stock',
        'store',
        'category',
        'created_at',
        'updated_at',
    )  # Columns to display in the product list

    list_filter = ('store', 'category', 'created_at')  # Filter options in sidebar
    search_fields = ('title', 'description')  # Enable search by title/description
    ordering = ('-created_at',)  # Default ordering
    list_editable = ("price", "stock")  # Fields editable directly in list view
    empty_value_display = "-خالی-"  # Display for empty fields