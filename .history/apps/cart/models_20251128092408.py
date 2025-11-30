from django.db import models
from apps.user.models import User
from apps.product.models import Product

# --------------------------------------------------------
# Cart Model
# --------------------------------------------------------
class Cart(models.Model):
    """
    Represents a shopping cart, which can be associated with a registered user or a session (guest).
    Tracks cart creation time and provides a total price property.
    """
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
        """
        Calculate the total price of all items in the cart.
        """
        return sum(item.total_price for item in self.items.all())


# --------------------------------------------------------
# CartItem Model
# --------------------------------------------------------
class CartItem(models.Model):
    """
    Represents a single product item in a cart.
    Tracks quantity and calculates the total price for the item.
    """
    cart = models.ForeignKey(
        Cart,
        on_delete=models.CASCADE,
        related_name="items"
    )
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)

    class Meta:
        unique_together = ('cart', 'product')  # Prevent duplicate products in the same cart
        verbose_name = "آیتم سبد خرید"
        verbose_name_plural = "آیتم‌های سبد خرید"

    def __str__(self):
        return f"{self.product.title} (x{self.quantity})"

    @property
    def total_price(self):
        """
        Calculate total price for this cart item.
        """
        return self.product.price * self.quantity