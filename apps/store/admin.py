from django.contrib import admin
from .models import Store

# Admin configuration for the Store model
@admin.register(Store)
class StoreAdmin(admin.ModelAdmin):
    list_display = ("store_name", "seller", "created_at")  # Fields shown in the admin list view
    search_fields = ("store_name", "seller__phone")        # Enable search by store name or seller phone
    ordering = ("-created_at",)                             # Default ordering: newest stores first