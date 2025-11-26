from django.contrib import admin
from .models import Order, OrderItem

# --------------------------------------------------------
# Inline admin for OrderItem within Order
# --------------------------------------------------------
class OrderItemInline(admin.TabularInline):
    """
    Allows editing of OrderItems directly from the Order admin page.
    All fields are read-only to prevent accidental modification.
    """
    model = OrderItem
    extra = 0  # Do not show extra blank forms
    readonly_fields = ("product", "unit_price", "quantity", "total_price")


# --------------------------------------------------------
# Admin configuration for Order model
# --------------------------------------------------------
@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    """
    Admin interface for managing Orders.
    Displays key order details and integrates OrderItem inlines.
    """
    list_display = ("id", "user", "status", "total_amount", "created_at")
    list_filter = ("status", "created_at")
    search_fields = ("user__phone",)
    inlines = [OrderItemInline]


# --------------------------------------------------------
# Admin configuration for OrderItem model
# --------------------------------------------------------
@admin.register(OrderItem)
class OrderItemAdmin(admin.ModelAdmin):
    """
    Admin interface for managing individual order items.
    """
    list_display = ("order", "product", "unit_price", "quantity", "total_price")