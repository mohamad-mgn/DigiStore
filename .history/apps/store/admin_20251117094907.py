from django.contrib import admin
from .models import Store


@admin.register(Store)
class StoreAdmin(admin.ModelAdmin):
    list_display = ("store_name", "seller", "created_at")
    search_fields = ("store_name", "seller__phone")
    ordering = ("-created_at",)