from django.db.models.signals import post_migrate
from django.dispatch import receiver
from .models import Category

@receiver(post_migrate)
def create_default_categories(sender, **kwargs):
    # Only run this for the 'product' app
    if sender.name == "apps.product":
        defaults = [
            ("لپ‌ تاپ", "laptop"),
            ("موبایل", "mobile"),
            ("تبلت", "tablet"),
        ]
        for name, slug in defaults:
            # get_or_create prevents duplicates
            Category.objects.get_or_create(name=name, slug=slug)