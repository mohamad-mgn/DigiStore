from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import User, CustomerProfile, SellerProfile

@receiver(post_save, sender=User)
def create_profiles(sender, instance, created, **kwargs):
    """
    هنگام ساخت هر کاربر، پروفایل‌های پایه را ایجاد می‌کنیم.
    اگر بعداً نخواستیم هر دو ایجاد شوند، می‌توانیم شرط is_seller را بررسی کنیم.
    """
    if created:
        # ایجاد پروفایل خریدار همیشه مفیده چون همهٔ کاربران می‌توانند خریدار باشند
        CustomerProfile.objects.get_or_create(user=instance)
        # پروفایل فروشنده را فقط زمانی ایجاد کن که is_seller = True
        # (اما اینجا برای دسترسی ساده هر دو را می‌سازیم؛ اگر نخواستید تغییر بده)
        SellerProfile.objects.get_or_create(user=instance)