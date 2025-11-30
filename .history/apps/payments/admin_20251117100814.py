from django.contrib import admin
from .models import Payment


@admin.register(Payment)
class PaymentAdmin(admin.ModelAdmin):
    list_display = ("id", "order", "amount", "status", "transaction_id", "created_at")
    list_filter = ("status", "gateway")
    search_fields = ("order__id", "transaction_id")