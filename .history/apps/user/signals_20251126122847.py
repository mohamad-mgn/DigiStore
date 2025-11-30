from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import User, CustomerProfile, SellerProfile


# Signal to automatically create profiles when a new user is created
@receiver(post_save, sender=User)
def create_profiles(sender, instance, created, **kwargs):
    if not created:
        return  # Only run for newly created users

    # Create a customer profile for every new user
    CustomerProfile.objects.get_or_create(user=instance)

    # If the user is a seller, also create a seller profile
    if instance.is_seller:
        SellerProfile.objects.get_or_create(user=instance)