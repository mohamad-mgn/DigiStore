from django.db import models
from apps.user.models import User

# Model representing a Store
class Store(models.Model):
    # Each seller can have only one store
    seller = models.OneToOneField(
        User,
        on_delete=models.CASCADE,
        related_name="store",
        verbose_name="Seller"
    )

    # Store name
    store_name = models.CharField("Store Name", max_length=200)
    # Optional description of the store
    description = models.TextField("Store Description", blank=True, null=True)

    # Timestamps for creation and last update
    created_at = models.DateTimeField("Created At", auto_now_add=True)
    updated_at = models.DateTimeField("Last Updated", auto_now=True)

    class Meta:
        verbose_name = "Store"
        verbose_name_plural = "Stores"
        ordering = ['-created_at']

    def __str__(self):
        return self.store_name