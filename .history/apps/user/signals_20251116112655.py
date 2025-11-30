from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import User, CustomerProfile, SellerProfile


@receiver(post_save, sender=User)
def create_role_profile(sender, instance, created, **kwargs):
    if not created:
        return

    # نقش از User مشخص است
    if instance.is_seller:
        SellerProfile.objects.create(user=instance)
    else:
        CustomerProfile.objects.create(user=instance)