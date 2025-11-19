from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import User, CustomerProfile, SellerProfile

@receiver(post_save, sender=User)
def create_profiles(sender, instance, created, **kwargs):
    """
    هنگام ساخت User جدید، یک CustomerProfile و یک SellerProfile ایجاد کن.
    (فروشنده لزوماً فوراً فعال نیست؛ سپس اطلاعات را تکمیل می‌کند.)
    """
    if created:
        CustomerProfile.objects.create(user=instance)
        SellerProfile.objects.create(user=instance)