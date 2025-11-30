from django.contrib import admin
from .models import Cart, CartItem

# --------------------------------------------------------
# Inline admin for CartItem
# --------------------------------------------------------
class CartItemInline(admin.TabularInline):
    """
    Display CartItem objects inline within the Cart admin page.
    """
    model = CartItem
    extra = 0  # Do not display extra empty forms


# --------------------------------------------------------
# Cart Admin
# --------------------------------------------------------
@admin.register(Cart)
class CartAdmin(admin.ModelAdmin):
    """
    Admin configuration for the Cart model.
    Shows key fields and embeds CartItem inline.
    """
    list_display = ("user", "created_at", "total_price")  # Columns to display in list view
    inlines = [CartItemInline]  # Show related cart items inline


# --------------------------------------------------------
# CartItem Admin
# --------------------------------------------------------
@admin.register(CartItem)
class CartItemAdmin(admin.ModelAdmin):
    """
    Admin configuration for individual CartItem objects.
    """
    list_display = ("cart", "product", "quantity", "total_price")  # Columns to display in list view
    list_filter = ("cart", "product")  # Filters for easy searching