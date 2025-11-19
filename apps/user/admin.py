from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as DjangoUserAdmin
from .models import User, CustomerProfile, SellerProfile


@admin.register(User)
class UserAdmin(DjangoUserAdmin):
    model = User
    list_display = ("phone", "full_name", "is_staff", "is_superuser", "is_seller")
    search_fields = ("phone", "full_name", "email")
    ordering = ("-date_joined",)

    fieldsets = (
        (None, {"fields": ("phone", "password")}),
        ("اطلاعات شخصی", {"fields": ("full_name", "email")}),
        ("دسترسی‌ها", {"fields": ("is_active", "is_staff", "is_superuser", "is_seller", "groups")}),
        ("اطلاعات زمانی", {"fields": ("date_joined",)}),
    )

    add_fieldsets = (
        (None, {
            "classes": ("wide",),
            "fields": ("phone", "password1", "password2", "is_staff", "is_superuser"),
        }),
    )


@admin.register(CustomerProfile)
class CustomerProfileAdmin(admin.ModelAdmin):
    list_display = ("user", "address", "postal_code")
    search_fields = ("user__phone", "user__full_name", "address")


@admin.register(SellerProfile)
class SellerProfileAdmin(admin.ModelAdmin):
    list_display = ("user", "store_name", "national_id")
    search_fields = ("user__phone", "store_name", "national_id")