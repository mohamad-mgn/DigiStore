# from django.contrib import admin
# from .models import Order, OrderItem


# class OrderItemInline(admin.TabularInline):
#     model = OrderItem
#     readonly_fields = ('product', 'unit_price', 'quantity')
#     extra = 0


# @admin.register(Order)
# class OrderAdmin(admin.ModelAdmin):
#     list_display = ('id', 'user', 'status', 'total_amount', 'created_at')
#     list_filter = ('status',)
#     search_fields = ('user__phone', 'id')
#     inlines = [OrderItemInline]


from django.apps import AppConfig

class OrdersConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'apps.orders'

    def ready(self):
        # اگر سیگنال دارید اینجا ایمپورت کنید
        import apps.orders.signals  # فقط در صورت وجود فایل signals.py