from django.db import models
from apps.user.models import User
from apps.product.models import Product


class Cart(models.Model):
    user = models.OneToOneField(
        User,
        on_delete=models.CASCADE,
        related_name="cart",
        verbose_name="کاربر"
    )
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = "سبد خرید"
        verbose_name_plural = "سبدهای خرید"

    def __str__(self):
        return f"سبد خرید {self.user.phone}"

    @property
    def total_price(self):
        # مجموع کل قیمت
        return sum(item.total_price for item in self.items.all())



class CartItem(models.Model):
    cart = models.ForeignKey(
        Cart,
        on_delete=models.CASCADE,
        related_name="items",
        verbose_name="سبد خرید"
    )
    product = models.ForeignKey(
        Product,
        on_delete=models.CASCADE,
        verbose_name="محصول"
    )
    quantity = models.PositiveIntegerField("تعداد", default=1)

    class Meta:
        verbose_name = "آیتم سبد خرید"
        verbose_name_plural = "آیتم‌های سبد خرید"
        unique_together = ('cart', 'product')

    def __str__(self):
        return f"{self.product.title} (x{self.quantity})"

    @property
    def total_price(self):
        return self.product.price * self.quantity