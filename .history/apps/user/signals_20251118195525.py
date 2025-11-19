from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import User, CustomerProfile, SellerProfile


@receiver(post_save, sender=User)
def create_profiles(sender, instance, created, **kwargs):
    if not created:
        return

    CustomerProfile.objects.get_or_create(user=instance)

    if instance.is_seller:
        SellerProfile.objects.get_or_create(user=instance)