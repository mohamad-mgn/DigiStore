from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as DjangoUserAdmin
from .models import User, CustomerProfile, SellerProfile

@admin.register(User)
class UserAdmin(DjangoUserAdmin):
    """
    سفارشی‌سازی نمایش مدل User در ادمین.
    نکته: DjangoUserAdmin به طور پیش‌فرض فیلدهایی مثل username را می‌بیند،
    ما اینجا فقط view اولیه را برای phone تنظیم کرده‌ایم.
    """
    model = User
    list_display = ('phone', 'full_name', 'is_staff', 'is_superuser')
    search_fields = ('phone', 'full_name')
    ordering = ('phone',)
    fieldsets = (
        (None, {'fields': ('phone', 'password')}),
        ('اطلاعات شخصی', {'fields': ('full_name', 'email')}),
        ('مجوزها', {'fields': ('is_active', 'is_staff', 'is_superuser')}),
    )
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('phone', 'password1', 'password2'),
        }),
    )

admin.site.register(CustomerProfile)
admin.site.register(SellerProfile)