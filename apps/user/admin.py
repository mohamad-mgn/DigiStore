from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as DjangoUserAdmin
from .models import User, CustomerProfile, SellerProfile


@admin.register(User)
class UserAdmin(DjangoUserAdmin):
    model = User
    # Columns displayed in the user list in admin
    list_display = ("phone", "full_name", "is_staff", "is_superuser", "is_seller")
    # Fields to search by in admin
    search_fields = ("phone", "full_name", "email")
    # Default ordering in admin
    ordering = ("-date_joined",)

    # Fieldsets for editing existing users
    fieldsets = (
        (None, {"fields": ("phone", "password")}),
        ("اطلاعات شخصی", {"fields": ("full_name", "email")}),
        ("دسترسی‌ها", {"fields": ("is_active", "is_staff", "is_superuser", "is_seller", "groups")}),
        ("اطلاعات زمانی", {"fields": ("date_joined",)}),
    )

    # Fieldsets for adding new users in admin
    add_fieldsets = (
        (None, {
            "classes": ("wide",),
            "fields": ("phone", "password1", "password2", "is_staff", "is_superuser"),
        }),
    )


@admin.register(CustomerProfile)
class CustomerProfileAdmin(admin.ModelAdmin):
    # Columns displayed for customer profiles in admin
    list_display = ("user", "address", "postal_code")
    # Fields to search by in customer profiles
    search_fields = ("user__phone", "user__full_name", "address")


@admin.register(SellerProfile)
class SellerProfileAdmin(admin.ModelAdmin):
     # Columns displayed for seller profiles in admin
    list_display = ("user", "store_name", "national_id")
    # Fields to search by in seller profiles
    search_fields = ("user__phone", "store_name", "national_id")