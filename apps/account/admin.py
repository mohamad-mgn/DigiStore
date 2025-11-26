from django.contrib import admin
from .models import MobileOTP

# --------------------------------------------------------
# MobileOTP Admin Configuration
# --------------------------------------------------------
@admin.register(MobileOTP)
class MobileOTPAdmin(admin.ModelAdmin):
    """
    Admin interface customization for MobileOTP model.
    Provides list display, filtering, searching, ordering, and readonly fields.
    """

    # Fields to display in the list view of the admin
    list_display = ('phone', 'code', 'created_at', 'verified', 'attempts')

    # Enable filtering by verification status and creation date
    list_filter = ('verified', 'created_at')

    # Enable search functionality on phone number and OTP code
    search_fields = ('phone', 'code')

    # Default ordering in the admin list view (newest first)
    ordering = ('-created_at',)

    # Make the created_at field read-only to prevent manual editing
    readonly_fields = ('created_at',)