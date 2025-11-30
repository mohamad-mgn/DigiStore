from django.contrib import admin
from .models import MobileOTP

@admin.register(MobileOTP)
class MobileOTPAdmin(admin.ModelAdmin):
    list_display = ('phone', 'code', 'created_at', 'verified', 'attempts')
    list_filter = ('verified', 'created_at')
    search_fields = ('phone', 'code')
    ordering = ('-created_at',)
    readonly_fields = ('created_at',)
