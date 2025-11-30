from django.db import models
from apps.user.models import User
from apps.product.models import Product

class Cart(models.Model):
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        null=True,
        blank=True,
        related_name="cart"
    )
    session_key = models.CharField(max_length=40, null=True, blank=True)

    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = "سبد خرید"
        verbose_name_plural = "سبدهای خرید"

    def __str__(self):
        if self.user:
            return f"سبد خرید {self.user.phone}"
        return f"سبد خرید مهمان ({self.session_key})"

    @property
    def total_price(self):
        return sum(item.total_price for item in self.items.all())


class CartItem(models.Model):
    cart = models.ForeignKey(
        Cart,
        on_delete=models.CASCADE,
        related_name="items"
    )
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)

    class Meta:
        unique_together = ('cart', 'product')

    def __str__(self):
        return f"{self.product.title} (x{self.quantity})"

    @property
    def total_price(self):
        return self.product.price * self.quantity