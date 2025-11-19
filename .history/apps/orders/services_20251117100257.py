# apps/orders/services.py
from apps.cart.models import Cart, CartItem
from .models import Order, OrderItem
from django.db import transaction


class OrderService:

    @staticmethod
    @transaction.atomic
    def create_order_from_cart(user, address=None, postal_code=None) -> Order:
        """
        سفارش جدید از سبد کاربر می‌سازد، آیتم‌ها را اضافه می‌کند و سبد را خالی می‌کند.
        """
        cart, _ = Cart.objects.get_or_create(user=user)
        items = cart.items.select_related('product').all()
        if not items:
            raise ValueError("سبد خرید خالی است.")

        total = sum(item.product.price * item.quantity for item in items)

        order = Order.objects.create(
            user=user,
            status='pending',
            total_amount=total,
            address=address or user.customer_profile.address,
            postal_code=postal_code or user.customer_profile.postal_code
        )

        order_items = []
        for it in items:
            order_items.append(OrderItem(
                order=order,
                product=it.product,
                unit_price=it.product.price,
                quantity=it.quantity
            ))
            # کاهش موجودی (اختیاری — می‌توان هنگام پرداخت انجام داد)
            if it.product.stock >= it.quantity:
                it.product.stock -= it.quantity
                it.product.save(update_fields=['stock'])
            else:
                # اگر موجودی کافی نبود خطا می‌زنیم
                raise ValueError(f"موجودی کافی برای {it.product.title} وجود ندارد.")

        OrderItem.objects.bulk_create(order_items)

        # پاک کردن سبد
        cart.items.all().delete()

        return order