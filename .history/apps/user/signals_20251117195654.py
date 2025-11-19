from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import User, CustomerProfile, SellerProfile


@receiver(post_save, sender=User)
def create_profiles(sender, instance, created, **kwargs):
    """
    هنگام ساخت کاربر:
      - اگر خریدار است → فقط CustomerProfile
      - اگر فروشنده است → CustomerProfile + SellerProfile
    """

    if not created:
        return

    # پروفایل خریدار برای همه ساخته می‌شود
    CustomerProfile.objects.get_or_create(user=instance)

    # پروفایل فروشنده فقط برای کاربران seller ساخته می‌شود
    if instance.is_seller:
        SellerProfile.objects.get_or_create(user=instance)