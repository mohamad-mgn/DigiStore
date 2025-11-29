from django.db.models.signals import post_migrate
from django.dispatch import receiver
from .models import Category

@receiver(post_migrate)
def create_default_categories(sender, **kwargs):
    if sender.name != "apps.product":
        return

    defaults = [
        ("لپ‌ تاپ", "laptop"),
        ("موبایل", "mobile"),
        ("تبلت", "tablet"),
    ]

    for name, slug in defaults:
        # Always search ONLY by slug (unique)
        Category.objects.get_or_create(
            slug=slug,
            defaults={"name": name}
        )