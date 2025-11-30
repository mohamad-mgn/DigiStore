from django.db import models
from apps.user.models import User

class Order(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='orders')
    created_at = models.DateTimeField(auto_now_add=True)
    paid = models.BooleanField(default=False)
    total_price = models.DecimalField(max_digits=12, decimal_places=2, default=0)

    def __str__(self):
        return f"Order #{self.id} - {self.user.phone}"

class OrderItem(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE, related_name='items')
    product_title = models.CharField(max_length=255)
    product_price = models.DecimalField(max_digits=12, decimal_places=2)
    quantity = models.PositiveIntegerField(default=1)