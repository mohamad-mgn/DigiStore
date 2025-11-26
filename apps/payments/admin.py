from django.contrib import admin
from .models import Payment


# ========================================================
# Admin interface for Payment model
# ========================================================
@admin.register(Payment)
class PaymentAdmin(admin.ModelAdmin):
    # Fields displayed in the list view
    list_display = ("id", "order", "amount", "status", "transaction_id", "created_at")

    # Fields available for filtering in the sidebar
    list_filter = ("status", "gateway")

    # Fields searchable via the search bar
    search_fields = ("order__id", "transaction_id")